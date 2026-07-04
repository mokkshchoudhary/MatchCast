"""Validate the raw MatchCast dataset and write its JSON report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from matchcast.ingestion.report import write_validation_report  # noqa: E402

SOURCE = PROJECT_ROOT / "data/raw/international_results.csv"
DESTINATION = PROJECT_ROOT / "reports/data_validation.json"


def main() -> int:
    """Generate the report and return a failing status for invalid data."""
    report = write_validation_report(SOURCE, DESTINATION)
    print(
        f"{report['status']}: {report['row_count']} rows, "
        f"{report['rejected_row_count']} rejected; wrote {DESTINATION}"
    )
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
