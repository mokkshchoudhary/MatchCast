"""Schema contracts for raw international match data."""

from typing import Final, TypedDict


class RawMatchRecord(TypedDict):
    """Minimum fields required from an international match data source."""

    date: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    tournament: str
    city: str
    country: str
    neutral: bool


REQUIRED_MATCH_COLUMNS: Final[tuple[str, ...]] = (
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
