"""Leakage-safe rolling team-form features for chronological match prediction.

All rolling statistics for a match are computed from that team's matches strictly
before the current one: every rolling window is preceded by a `shift(1)` so the
current match's own goals, result, and rating can never leak into its own features.
"""

from __future__ import annotations

import pandas as pd

DEFAULT_WINDOW = 5

_RESULT_POINTS = {"H": 1.0, "D": 0.5, "A": 0.0}

_QUALIFIER_MARKER = "qualif"
_WORLD_CUP = "FIFA World Cup"
_CONTINENTAL_MARKERS = (
    "Copa América",
    "Copa America",
    "African Cup of Nations",
    "AFC Asian Cup",
    "UEFA Euro",
    "European Championship",
    "Gold Cup",
    "Oceania",
    "Nations League",
)


def classify_tournament_type(tournament: str) -> str:
    """Bucket a raw tournament label into a small, model-friendly category."""
    name = str(tournament)
    lowered = name.lower()
    if _QUALIFIER_MARKER in lowered:
        return "qualifier"
    if name == _WORLD_CUP:
        return "world_cup"
    if any(marker.lower() in lowered for marker in _CONTINENTAL_MARKERS):
        return "continental"
    if lowered == "friendly":
        return "friendly"
    return "other"


def build_team_match_panel(matches: pd.DataFrame) -> pd.DataFrame:
    """Reshape one row per match into two rows per match: one per participating team."""
    required = {
        "match_id", "date", "home_team", "away_team", "home_score", "away_score",
        "neutral", "result", "home_elo", "away_elo",
    }
    if not required <= set(matches.columns):
        raise ValueError(f"matches is missing required columns: {required - set(matches.columns)}")

    home_rows = pd.DataFrame({
        "match_id": matches["match_id"],
        "date": matches["date"],
        "team": matches["home_team"],
        "opponent": matches["away_team"],
        "is_home": True,
        "goals_for": matches["home_score"].astype(float),
        "goals_against": matches["away_score"].astype(float),
        "team_elo": matches["home_elo"],
        "opponent_elo": matches["away_elo"],
        "result_points": matches["result"].map(_RESULT_POINTS),
        "expected_points": matches["elo_home_probability"] + 0.5 * matches["elo_draw_probability"],
    })
    away_rows = pd.DataFrame({
        "match_id": matches["match_id"],
        "date": matches["date"],
        "team": matches["away_team"],
        "opponent": matches["home_team"],
        "is_home": False,
        "goals_for": matches["away_score"].astype(float),
        "goals_against": matches["home_score"].astype(float),
        "team_elo": matches["away_elo"],
        "opponent_elo": matches["home_elo"],
        "result_points": 1.0 - matches["result"].map(_RESULT_POINTS),
        "expected_points": matches["elo_away_probability"] + 0.5 * matches["elo_draw_probability"],
    })
    panel = pd.concat([home_rows, away_rows], ignore_index=True)
    return panel.sort_values(["team", "date", "match_id"], kind="mergesort").reset_index(drop=True)


def add_rolling_features(panel: pd.DataFrame, window: int = DEFAULT_WINDOW) -> pd.DataFrame:
    """Add shift(1)-then-rolling team-form columns; a team's own match never leaks."""
    if window < 1:
        raise ValueError("window must be at least 1")
    ordered = panel.sort_values(["team", "date", "match_id"], kind="mergesort").reset_index(drop=True)
    grouped = ordered.groupby("team", sort=False)

    def prior_rolling_mean(column: str) -> pd.Series:
        return grouped[column].transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())

    ordered["rolling_goals_for"] = prior_rolling_mean("goals_for").fillna(0.0)
    ordered["rolling_goals_against"] = prior_rolling_mean("goals_against").fillna(0.0)
    ordered["rolling_win_rate"] = prior_rolling_mean("result_points").fillna(0.5)
    ordered["rolling_form_vs_expected"] = (
        grouped["result_points"].transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
        - grouped["expected_points"].transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    ).fillna(0.0)
    prior_elo = grouped["team_elo"].shift(1)
    elo_n_ago = grouped["team_elo"].shift(1 + window)
    ordered["rolling_elo_trend"] = (prior_elo - elo_n_ago).fillna(0.0)
    return ordered


def build_match_features(matches: pd.DataFrame, window: int = DEFAULT_WINDOW) -> pd.DataFrame:
    """Return the match-level frame augmented with leakage-safe home/away rolling features."""
    panel = add_rolling_features(build_team_match_panel(matches), window=window)
    feature_columns = [
        "rolling_goals_for", "rolling_goals_against", "rolling_win_rate",
        "rolling_form_vs_expected", "rolling_elo_trend",
    ]
    home_features = panel.loc[panel["is_home"], ["match_id", *feature_columns]].rename(
        columns={col: f"home_{col}" for col in feature_columns}
    )
    away_features = panel.loc[~panel["is_home"], ["match_id", *feature_columns]].rename(
        columns={col: f"away_{col}" for col in feature_columns}
    )
    enriched = matches.merge(home_features, on="match_id", how="left").merge(
        away_features, on="match_id", how="left"
    )
    enriched["tournament_type"] = enriched["tournament"].map(classify_tournament_type)
    return enriched
