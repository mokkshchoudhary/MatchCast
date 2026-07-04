"""Validation rules for raw international match data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from matchcast.ingestion.schema import REQUIRED_MATCH_COLUMNS

MISSING_SCORE_VALUES = frozenset({"", "na", "n/a", "null", "none"})
VALID_NEUTRAL_VALUES = frozenset({"true", "false"})


@dataclass(frozen=True)
class ValidationIssue:
    """A grouped validation failure."""

    code: str
    count: int
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Summary of validation performed on a raw match table."""

    row_count: int
    completed_match_count: int
    scheduled_fixture_count: int
    rejected_row_count: int
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        """Return whether no validation failures were found."""
        return not self.issues


def _normalized_strings(series: pd.Series) -> pd.Series:
    return series.fillna("").astype("string").str.strip().str.lower()


def validate_matches(matches: pd.DataFrame) -> ValidationResult:
    """Validate the minimum raw schema and supported row values."""
    issues: list[ValidationIssue] = []
    missing_columns = [
        column for column in REQUIRED_MATCH_COLUMNS if column not in matches.columns
    ]
    if missing_columns:
        issues.append(
            ValidationIssue(
                code="missing_columns",
                count=len(missing_columns),
                message=f"Missing required columns: {', '.join(missing_columns)}",
            )
        )
        return ValidationResult(
            row_count=len(matches),
            completed_match_count=0,
            scheduled_fixture_count=0,
            rejected_row_count=len(matches),
            issues=tuple(issues),
        )

    invalid_rows = pd.Series(False, index=matches.index, dtype=bool)
    parsed_dates = pd.to_datetime(
        matches["date"].fillna("").astype("string").str.strip(),
        format="%Y-%m-%d",
        errors="coerce",
    )
    invalid_date_count = int(parsed_dates.isna().sum())
    if invalid_date_count:
        invalid_rows |= parsed_dates.isna()
        issues.append(
            ValidationIssue(
                code="invalid_dates",
                count=invalid_date_count,
                message="Dates must use a valid YYYY-MM-DD value.",
            )
        )

    for column in ("home_team", "away_team"):
        empty_mask = matches[column].fillna("").astype("string").str.strip().eq("")
        empty_count = int(empty_mask.sum())
        if empty_count:
            invalid_rows |= empty_mask
            issues.append(
                ValidationIssue(
                    code=f"empty_{column}",
                    count=empty_count,
                    message=f"{column} must not be empty.",
                )
            )

    home_scores = _normalized_strings(matches["home_score"])
    away_scores = _normalized_strings(matches["away_score"])
    home_missing = home_scores.isin(MISSING_SCORE_VALUES)
    away_missing = away_scores.isin(MISSING_SCORE_VALUES)
    partial_score_count = int((home_missing ^ away_missing).sum())
    if partial_score_count:
        invalid_rows |= home_missing ^ away_missing
        issues.append(
            ValidationIssue(
                code="partial_scores",
                count=partial_score_count,
                message="A row must provide both scores or neither score.",
            )
        )

    completed_mask = ~home_missing & ~away_missing
    scheduled_mask = home_missing & away_missing
    numeric_home = pd.to_numeric(home_scores.where(completed_mask), errors="coerce")
    numeric_away = pd.to_numeric(away_scores.where(completed_mask), errors="coerce")
    invalid_numeric_mask = completed_mask & (numeric_home.isna() | numeric_away.isna())
    invalid_numeric_count = int(invalid_numeric_mask.sum())
    if invalid_numeric_count:
        invalid_rows |= invalid_numeric_mask
        issues.append(
            ValidationIssue(
                code="non_numeric_scores",
                count=invalid_numeric_count,
                message="Completed-match scores must be numeric.",
            )
        )

    valid_numeric_mask = completed_mask & ~invalid_numeric_mask
    negative_score_count = int(
        (
            valid_numeric_mask
            & ((numeric_home < 0).fillna(False) | (numeric_away < 0).fillna(False))
        ).sum()
    )
    if negative_score_count:
        invalid_rows |= valid_numeric_mask & (
            (numeric_home < 0).fillna(False) | (numeric_away < 0).fillna(False)
        )
        issues.append(
            ValidationIssue(
                code="negative_scores",
                count=negative_score_count,
                message="Scores must be non-negative.",
            )
        )

    fractional_score_count = int(
        (
            valid_numeric_mask
            & (
                (numeric_home.mod(1) != 0).fillna(False)
                | (numeric_away.mod(1) != 0).fillna(False)
            )
        ).sum()
    )
    if fractional_score_count:
        invalid_rows |= valid_numeric_mask & (
            (numeric_home.mod(1) != 0).fillna(False)
            | (numeric_away.mod(1) != 0).fillna(False)
        )
        issues.append(
            ValidationIssue(
                code="fractional_scores",
                count=fractional_score_count,
                message="Scores must be whole numbers.",
            )
        )

    neutral_values = _normalized_strings(matches["neutral"])
    invalid_neutral_count = int((~neutral_values.isin(VALID_NEUTRAL_VALUES)).sum())
    if invalid_neutral_count:
        invalid_rows |= ~neutral_values.isin(VALID_NEUTRAL_VALUES)
        issues.append(
            ValidationIssue(
                code="invalid_neutral",
                count=invalid_neutral_count,
                message="neutral must be TRUE or FALSE.",
            )
        )

    return ValidationResult(
        row_count=len(matches),
        completed_match_count=int(completed_mask.sum()),
        scheduled_fixture_count=int(scheduled_mask.sum()),
        rejected_row_count=int(invalid_rows.sum()),
        issues=tuple(issues),
    )


def load_and_validate(path: Path) -> ValidationResult:
    """Load raw strings from a CSV file and validate them."""
    matches = pd.read_csv(path, dtype="string", keep_default_na=False)
    return validate_matches(matches)
