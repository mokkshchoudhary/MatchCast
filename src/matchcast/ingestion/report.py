"""Machine-readable reporting for raw match validation."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from matchcast.ingestion.download_results import calculate_sha256
from matchcast.ingestion.schema import REQUIRED_MATCH_COLUMNS
from matchcast.ingestion.validation import MISSING_SCORE_VALUES, validate_matches


def build_validation_report(path: Path) -> dict[str, Any]:
    """Build a serializable validation report for a raw CSV snapshot."""
    matches = pd.read_csv(path, dtype="string", keep_default_na=False)
    result = validate_matches(matches)
    parsed_dates = pd.to_datetime(
        matches["date"].astype("string").str.strip(),
        format="%Y-%m-%d",
        errors="coerce",
    )

    missing_values: dict[str, int] = {}
    for column in REQUIRED_MATCH_COLUMNS:
        if column not in matches.columns:
            missing_values[column] = len(matches)
            continue
        normalized = matches[column].fillna("").astype("string").str.strip().str.lower()
        missing_values[column] = int(normalized.isin(MISSING_SCORE_VALUES).sum())

    valid_dates = parsed_dates.dropna()
    date_range = {
        "minimum": valid_dates.min().date().isoformat() if not valid_dates.empty else None,
        "maximum": valid_dates.max().date().isoformat() if not valid_dates.empty else None,
    }

    return {
        "source_path": path.as_posix(),
        "sha256": calculate_sha256(path),
        "status": "valid" if result.is_valid else "invalid",
        "row_count": result.row_count,
        "completed_match_count": result.completed_match_count,
        "scheduled_fixture_count": result.scheduled_fixture_count,
        "rejected_row_count": result.rejected_row_count,
        "columns": list(matches.columns),
        "date_range": date_range,
        "missing_values": missing_values,
        "issues": [asdict(issue) for issue in result.issues],
    }


def write_validation_report(source: Path, destination: Path) -> dict[str, Any]:
    """Write a deterministic, human-readable JSON validation report."""
    report = build_validation_report(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report
