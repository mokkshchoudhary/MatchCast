"""Tests for the training-period outcome frequency baseline."""

import numpy as np
import pandas as pd
import pytest

from matchcast.evaluation.baseline import TrainingFrequencyBaseline


def test_fit_recovers_exact_frequencies() -> None:
    train = pd.Series(["H", "H", "H", "D", "A"])
    baseline = TrainingFrequencyBaseline.fit(train)
    assert baseline.probabilities == pytest.approx((0.6, 0.2, 0.2))


def test_predict_broadcasts_same_row_to_every_match() -> None:
    train = pd.Series(["H", "D", "A", "A"])
    baseline = TrainingFrequencyBaseline.fit(train)
    predictions = baseline.predict(5)
    assert predictions.shape == (5, 3)
    assert np.allclose(predictions, predictions[0])
    assert np.allclose(predictions.sum(axis=1), 1.0)


def test_fit_rejects_empty_training_set() -> None:
    with pytest.raises(ValueError):
        TrainingFrequencyBaseline.fit(pd.Series([], dtype=str))


def test_fit_handles_missing_class_as_zero() -> None:
    train = pd.Series(["H", "H", "A"])
    baseline = TrainingFrequencyBaseline.fit(train)
    assert baseline.probabilities[1] == pytest.approx(0.0)
