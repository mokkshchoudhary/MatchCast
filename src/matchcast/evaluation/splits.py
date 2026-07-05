"""Chronological split and expanding-window backtest boundaries."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ChronologicalSplit:
    """Train/validation/test row indices with no overlap and no future leakage."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def chronological_split(
    frame: pd.DataFrame,
    date_column: str,
    validation_fraction: float = 0.15,
    test_fraction: float = 0.15,
) -> ChronologicalSplit:
    """Split a date-sorted frame into train/validation/test by position, not randomly."""
    if not (0.0 < validation_fraction < 1.0) or not (0.0 < test_fraction < 1.0):
        raise ValueError("fractions must be between 0 and 1")
    if validation_fraction + test_fraction >= 1.0:
        raise ValueError("validation_fraction + test_fraction must leave a non-empty train set")
    ordered = frame.sort_values(date_column, kind="mergesort").reset_index(drop=True)
    n = len(ordered)
    test_start = int(n * (1.0 - test_fraction))
    validation_start = int(n * (1.0 - test_fraction - validation_fraction))
    train = ordered.iloc[:validation_start].copy()
    validation = ordered.iloc[validation_start:test_start].copy()
    test = ordered.iloc[test_start:].copy()
    if len(train) and len(validation):
        assert train[date_column].max() <= validation[date_column].min()
    if len(validation) and len(test):
        assert validation[date_column].max() <= test[date_column].min()
    return ChronologicalSplit(train=train, validation=validation, test=test)


def expanding_window_tournament_folds(
    frame: pd.DataFrame,
    date_column: str,
    tournament_column: str,
    tournament_name: str,
    years: list[int],
) -> list[tuple[int, pd.DataFrame, pd.DataFrame]]:
    """Build one expanding-window fold per requested tournament year.

    For each year, the test fold is every match of `tournament_name` played in that
    year; the train fold is every match strictly before the test fold's earliest date.
    Years absent from the data are skipped so callers can request a superset safely.
    """
    ordered = frame.sort_values(date_column, kind="mergesort").reset_index(drop=True)
    dates = ordered[date_column]
    is_tournament = ordered[tournament_column] == tournament_name
    folds: list[tuple[int, pd.DataFrame, pd.DataFrame]] = []
    for year in years:
        test = ordered.loc[is_tournament & (dates.dt.year == year)]
        if test.empty:
            continue
        cutoff = test[date_column].min()
        train = ordered.loc[dates < cutoff]
        if train.empty:
            continue
        assert train[date_column].max() < test[date_column].min()
        folds.append((year, train.copy(), test.copy()))
    return folds
