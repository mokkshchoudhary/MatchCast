"""Tests for leakage-safe rolling team-form features."""

import pandas as pd
import pytest

from matchcast.features.rolling import (
    build_match_features,
    build_team_match_panel,
    classify_tournament_type,
    add_rolling_features,
)


@pytest.mark.parametrize(
    ("tournament", "expected"),
    [
        ("FIFA World Cup", "world_cup"),
        ("FIFA World Cup qualification", "qualifier"),
        ("UEFA Euro qualification", "qualifier"),
        ("UEFA Euro", "continental"),
        ("Copa América", "continental"),
        ("Friendly", "friendly"),
        ("British Home Championship", "other"),
    ],
)
def test_classify_tournament_type(tournament: str, expected: str) -> None:
    assert classify_tournament_type(tournament) == expected


def _matches(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    frame["date"] = pd.to_datetime(frame["date"])
    return frame


def _team_a_history() -> pd.DataFrame:
    return _matches([
        {"match_id": "m1", "date": "2020-01-01", "home_team": "A", "away_team": "B",
         "home_score": 3, "away_score": 0, "neutral": False, "result": "H",
         "home_elo": 1500.0, "away_elo": 1500.0,
         "elo_home_probability": 0.6, "elo_draw_probability": 0.25, "elo_away_probability": 0.15,
         "tournament": "Friendly"},
        {"match_id": "m2", "date": "2020-02-01", "home_team": "A", "away_team": "C",
         "home_score": 1, "away_score": 1, "neutral": False, "result": "D",
         "home_elo": 1520.0, "away_elo": 1500.0,
         "elo_home_probability": 0.6, "elo_draw_probability": 0.25, "elo_away_probability": 0.15,
         "tournament": "Friendly"},
        {"match_id": "m3", "date": "2020-03-01", "home_team": "A", "away_team": "D",
         "home_score": 2, "away_score": 2, "neutral": False, "result": "D",
         "home_elo": 1515.0, "away_elo": 1500.0,
         "elo_home_probability": 0.6, "elo_draw_probability": 0.25, "elo_away_probability": 0.15,
         "tournament": "Friendly"},
    ])


def test_build_team_match_panel_has_two_rows_per_match_with_swapped_goals() -> None:
    panel = build_team_match_panel(_team_a_history())
    assert len(panel) == 6
    m1_home = panel[(panel["match_id"] == "m1") & (panel["team"] == "A")].iloc[0]
    m1_away = panel[(panel["match_id"] == "m1") & (panel["team"] == "B")].iloc[0]
    assert m1_home["goals_for"] == 3 and m1_home["goals_against"] == 0
    assert m1_away["goals_for"] == 0 and m1_away["goals_against"] == 3
    assert m1_home["result_points"] == 1.0 and m1_away["result_points"] == 0.0


def test_first_match_gets_default_fallback_features() -> None:
    panel = add_rolling_features(build_team_match_panel(_team_a_history()), window=5)
    first = panel[(panel["match_id"] == "m1") & (panel["team"] == "A")].iloc[0]
    assert first["rolling_goals_for"] == 0.0
    assert first["rolling_goals_against"] == 0.0
    assert first["rolling_win_rate"] == 0.5
    assert first["rolling_elo_trend"] == 0.0


def test_rolling_features_use_only_strictly_prior_matches() -> None:
    panel = add_rolling_features(build_team_match_panel(_team_a_history()), window=5)
    third = panel[(panel["match_id"] == "m3") & (panel["team"] == "A")].iloc[0]
    # Team A's first two matches (as home team) scored 3 and 1 goals, conceded 0 and 1.
    assert third["rolling_goals_for"] == pytest.approx((3 + 1) / 2)
    assert third["rolling_goals_against"] == pytest.approx((0 + 1) / 2)
    assert third["rolling_win_rate"] == pytest.approx((1.0 + 0.5) / 2)


def test_changing_a_future_result_does_not_change_earlier_rolling_features() -> None:
    history = _team_a_history()
    changed = history.copy()
    changed.loc[changed["match_id"] == "m3", ["home_score", "away_score", "result"]] = [5, 0, "H"]

    before = add_rolling_features(build_team_match_panel(history), window=5)
    after = add_rolling_features(build_team_match_panel(changed), window=5)

    cols = ["rolling_goals_for", "rolling_goals_against", "rolling_win_rate", "rolling_elo_trend"]
    before_early = before[before["match_id"].isin(["m1", "m2"])].sort_values(["match_id", "team"])
    after_early = after[after["match_id"].isin(["m1", "m2"])].sort_values(["match_id", "team"])
    pd.testing.assert_frame_equal(
        before_early[cols].reset_index(drop=True), after_early[cols].reset_index(drop=True)
    )


def test_rolling_features_respect_window_size() -> None:
    history = _team_a_history()
    window_1 = add_rolling_features(build_team_match_panel(history), window=1)
    third = window_1[(window_1["match_id"] == "m3") & (window_1["team"] == "A")].iloc[0]
    # With window=1 only the immediately preceding match (m2: 1 scored, 1 conceded) counts.
    assert third["rolling_goals_for"] == pytest.approx(1.0)
    assert third["rolling_goals_against"] == pytest.approx(1.0)


def test_build_match_features_adds_home_away_columns_and_tournament_type() -> None:
    enriched = build_match_features(_team_a_history(), window=5)
    for prefix in ("home", "away"):
        for column in ("rolling_goals_for", "rolling_goals_against", "rolling_win_rate",
                       "rolling_form_vs_expected", "rolling_elo_trend"):
            assert f"{prefix}_{column}" in enriched.columns
    assert "tournament_type" in enriched.columns
    assert (enriched["tournament_type"] == "friendly").all()
    assert len(enriched) == len(_team_a_history())


def test_build_match_features_rejects_missing_columns() -> None:
    with pytest.raises(ValueError):
        build_match_features(pd.DataFrame({"match_id": ["m1"]}))
