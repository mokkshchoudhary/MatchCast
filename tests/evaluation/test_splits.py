"""Tests for chronological split and expanding-window backtest boundaries."""

import pandas as pd
import pytest

from matchcast.evaluation.splits import chronological_split, expanding_window_tournament_folds


def _make_frame(n: int) -> pd.DataFrame:
    dates = pd.date_range("2000-01-01", periods=n, freq="D")
    return pd.DataFrame({"date": dates, "value": range(n)})


def test_chronological_split_sizes_and_order() -> None:
    frame = _make_frame(100)
    result = chronological_split(frame, "date", validation_fraction=0.2, test_fraction=0.1)
    assert len(result.train) + len(result.validation) + len(result.test) == 100
    assert result.train["date"].max() <= result.validation["date"].min()
    assert result.validation["date"].max() <= result.test["date"].min()


def test_chronological_split_rejects_invalid_fractions() -> None:
    frame = _make_frame(10)
    with pytest.raises(ValueError):
        chronological_split(frame, "date", validation_fraction=0.6, test_fraction=0.6)
    with pytest.raises(ValueError):
        chronological_split(frame, "date", validation_fraction=0.0, test_fraction=0.2)


def test_chronological_split_is_deterministic_regardless_of_input_order() -> None:
    frame = _make_frame(50)
    shuffled = frame.sample(frac=1.0, random_state=1).reset_index(drop=True)
    a = chronological_split(frame, "date")
    b = chronological_split(shuffled, "date")
    pd.testing.assert_frame_equal(a.train.reset_index(drop=True), b.train.reset_index(drop=True))
    pd.testing.assert_frame_equal(a.test.reset_index(drop=True), b.test.reset_index(drop=True))


def test_expanding_window_folds_train_strictly_precedes_test() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2010-01-01", "2013-06-01", "2014-06-01", "2014-06-02", "2017-06-01", "2018-06-01"]
            ),
            "tournament": ["Friendly", "Friendly", "FIFA World Cup", "FIFA World Cup", "Friendly", "FIFA World Cup"],
        }
    )
    folds = expanding_window_tournament_folds(frame, "date", "tournament", "FIFA World Cup", [2014, 2018, 2022])
    years = [year for year, _, _ in folds]
    assert years == [2014, 2018]
    for year, train, test in folds:
        assert train["date"].max() < test["date"].min()
        assert (test["tournament"] == "FIFA World Cup").all()
        assert (test["date"].dt.year == year).all()


def test_expanding_window_folds_skip_missing_years() -> None:
    frame = pd.DataFrame(
        {"date": pd.to_datetime(["2014-06-01"]), "tournament": ["FIFA World Cup"]}
    )
    folds = expanding_window_tournament_folds(frame, "date", "tournament", "FIFA World Cup", [2010, 2014])
    assert [year for year, _, _ in folds] == []


def test_expanding_window_folds_grow_with_each_year() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2010-01-01", "2014-06-01", "2016-01-01", "2018-06-01"]),
            "tournament": ["Friendly", "FIFA World Cup", "Friendly", "FIFA World Cup"],
        }
    )
    folds = expanding_window_tournament_folds(frame, "date", "tournament", "FIFA World Cup", [2014, 2018])
    sizes = {year: len(train) for year, train, _ in folds}
    assert sizes[2018] > sizes[2014]
