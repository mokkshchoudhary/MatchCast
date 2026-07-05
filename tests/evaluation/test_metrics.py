"""Tests for probabilistic evaluation metrics."""

import numpy as np
import pytest

from matchcast.evaluation.metrics import (
    accuracy,
    calibration_curve,
    goal_mae,
    multiclass_brier_score,
    multiclass_log_loss,
    poisson_negative_log_likelihood,
)


def test_log_loss_matches_hand_computation() -> None:
    results = np.array(["H", "D", "A"])
    probs = np.array([[0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.1, 0.8]])
    expected = -np.mean(np.log([0.8, 0.6, 0.8]))
    assert multiclass_log_loss(results, probs) == pytest.approx(expected)


def test_log_loss_penalizes_confident_wrong_predictions() -> None:
    results = np.array(["H", "H"])
    confident_right = np.array([[0.99, 0.005, 0.005], [0.99, 0.005, 0.005]])
    confident_wrong = np.array([[0.01, 0.01, 0.98], [0.01, 0.01, 0.98]])
    assert multiclass_log_loss(results, confident_right) < multiclass_log_loss(results, confident_wrong)


def test_brier_score_zero_for_perfect_predictions() -> None:
    results = np.array(["H", "A"])
    probs = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert multiclass_brier_score(results, probs) == pytest.approx(0.0)


def test_brier_score_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        multiclass_brier_score(np.array(["H"]), np.array([[0.5, 0.5]]))


def test_accuracy_counts_argmax_matches() -> None:
    results = np.array(["H", "D", "A", "A"])
    probs = np.array(
        [[0.7, 0.2, 0.1], [0.2, 0.7, 0.1], [0.1, 0.2, 0.7], [0.5, 0.3, 0.2]]
    )
    assert accuracy(results, probs) == pytest.approx(0.75)


def test_goal_mae_basic() -> None:
    actual = np.array([2.0, 1.0, 0.0])
    predicted = np.array([1.5, 1.0, 1.0])
    assert goal_mae(actual, predicted) == pytest.approx((0.5 + 0.0 + 1.0) / 3)


def test_goal_mae_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        goal_mae(np.array([1.0]), np.array([1.0, 2.0]))


def test_poisson_nll_lower_for_correct_rate() -> None:
    actual = np.array([2.0, 2.0, 2.0, 2.0])
    good_rate = np.full(4, 2.0)
    bad_rate = np.full(4, 0.1)
    assert poisson_negative_log_likelihood(actual, good_rate) < poisson_negative_log_likelihood(
        actual, bad_rate
    )


def test_calibration_curve_perfect_calibration() -> None:
    rng = np.random.default_rng(0)
    n = 4000
    predicted_home_prob = rng.uniform(0.0, 1.0, size=n)
    is_home = rng.uniform(0.0, 1.0, size=n) < predicted_home_prob
    results = np.where(is_home, "H", "A")
    probs = np.column_stack([predicted_home_prob, np.zeros(n), 1.0 - predicted_home_prob])
    curve = calibration_curve(results, probs, class_index=0, n_bins=10)
    assert np.allclose(curve["mean_predicted"], curve["observed_frequency"], atol=0.08)
    assert curve["count"].sum() == n


def test_calibration_curve_drops_empty_bins() -> None:
    results = np.array(["H", "H", "A"])
    probs = np.array([[0.05, 0.0, 0.95], [0.05, 0.0, 0.95], [0.05, 0.0, 0.95]])
    curve = calibration_curve(results, probs, class_index=0, n_bins=10)
    assert len(curve["mean_predicted"]) == 1
