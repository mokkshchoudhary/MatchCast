"""Tests for machine-readable validation reports."""

from __future__ import annotations

import json
from pathlib import Path

from matchcast.ingestion.report import build_validation_report, write_validation_report


def test_build_validation_report_summarizes_source(tmp_path: Path) -> None:
    """The report should expose counts, dates, missing values, and validity."""
    source = tmp_path / "results.csv"
    source.write_text(
        "date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n"
        "2026-07-03,Argentina,Egypt,2,1,FIFA World Cup,Atlanta,United States,TRUE\n"
        "2026-07-04,Canada,Morocco,NA,NA,FIFA World Cup,Houston,United States,TRUE\n",
        encoding="utf-8",
    )

    report = build_validation_report(source)

    assert report["status"] == "valid"
    assert report["row_count"] == 2
    assert report["completed_match_count"] == 1
    assert report["scheduled_fixture_count"] == 1
    assert report["rejected_row_count"] == 0
    assert report["date_range"] == {
        "minimum": "2026-07-03",
        "maximum": "2026-07-04",
    }
    assert report["missing_values"]["home_score"] == 1
    assert report["missing_values"]["away_score"] == 1
    assert report["issues"] == []


def test_write_validation_report_outputs_json(tmp_path: Path) -> None:
    """The written report should be valid JSON and end with a newline."""
    source = tmp_path / "results.csv"
    destination = tmp_path / "report.json"
    source.write_text(
        "date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n"
        "bad-date,,Morocco,-1,0,FIFA World Cup,Houston,United States,maybe\n",
        encoding="utf-8",
    )

    report = write_validation_report(source, destination)

    assert report["status"] == "invalid"
    assert report["rejected_row_count"] == 1
    assert json.loads(destination.read_text(encoding="utf-8")) == report
    assert destination.read_bytes().endswith(b"\n")
