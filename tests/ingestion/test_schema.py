"""Tests for the raw match schema contract."""

from matchcast.ingestion.schema import REQUIRED_MATCH_COLUMNS


def test_required_match_columns_are_complete_and_unique() -> None:
    """The source contract should expose the agreed minimum fields once."""
    assert REQUIRED_MATCH_COLUMNS == (
        "date",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "tournament",
        "city",
        "country",
        "neutral",
    )
    assert len(REQUIRED_MATCH_COLUMNS) == len(set(REQUIRED_MATCH_COLUMNS))
