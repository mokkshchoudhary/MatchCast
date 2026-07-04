"""Tests for raw match validation."""

from __future__ import annotations

import pandas as pd

from matchcast.ingestion.validation import validate_matches


def make_match(**overrides: object) -> dict[str, object]:
    """Build a valid raw completed-match record."""
    match: dict[str, object] = {
        "date": "2026-07-04",
        "home_team": "Canada",
        "away_team": "Morocco",
        "home_score": "1",
        "away_score": "0",
        "tournament": "FIFA World Cup",
        "city": "Houston",
        "country": "United States",
        "neutral": "TRUE",
    }
    match.update(overrides)
    return match


def issue_codes(matches: list[dict[str, object]]) -> set[str]:
    """Return issue codes for a list of raw records."""
    return {issue.code for issue in validate_matches(pd.DataFrame(matches)).issues}


def test_valid_completed_match_and_scheduled_fixture() -> None:
    """Completed matches and fixtures with two missing scores are supported."""
    result = validate_matches(
        pd.DataFrame(
            [
                make_match(),
                make_match(home_score="NA", away_score="NA"),
            ]
        )
    )

    assert result.is_valid
    assert result.completed_match_count == 1
    assert result.scheduled_fixture_count == 1
    assert result.rejected_row_count == 0


def test_missing_required_column_stops_row_validation() -> None:
    """A missing schema field should produce a grouped schema issue."""
    match = make_match()
    del match["neutral"]

    result = validate_matches(pd.DataFrame([match]))

    assert not result.is_valid
    assert result.issues[0].code == "missing_columns"
    assert "neutral" in result.issues[0].message
    assert result.rejected_row_count == 1


def test_invalid_dates_and_team_names_are_rejected() -> None:
    """Dates must parse strictly and both team names must be present."""
    codes = issue_codes(
        [
            make_match(date="2026-02-30", home_team=" "),
            make_match(date="", away_team=None),
        ]
    )

    assert {"invalid_dates", "empty_home_team", "empty_away_team"} <= codes


def test_partial_non_numeric_negative_and_fractional_scores_are_rejected() -> None:
    """Only paired, non-negative integer scores are valid."""
    codes = issue_codes(
        [
            make_match(home_score="NA", away_score="1"),
            make_match(home_score="two", away_score="1"),
            make_match(home_score="-1", away_score="1"),
            make_match(home_score="1.5", away_score="1"),
        ]
    )

    assert {
        "partial_scores",
        "non_numeric_scores",
        "negative_scores",
        "fractional_scores",
    } <= codes


def test_neutral_flag_is_strictly_boolean() -> None:
    """Common truthy values other than TRUE/FALSE should not be accepted."""
    assert "invalid_neutral" in issue_codes([make_match(neutral="yes")])
