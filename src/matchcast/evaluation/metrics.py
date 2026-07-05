"""Probabilistic evaluation metrics for chronological match backtests."""

from __future__ import annotations

import numpy as np

CLASS_ORDER: tuple[str, str, str] = ("H", "D", "A")


def _one_hot(results: np.ndarray, labels: tuple[str, ...] = CLASS_ORDER) -> np.ndarray:
    results = np.asarray(results)
    return np.column_stack([(results == label).astype(float) for label in labels])


def multiclass_log_loss(
    results: np.ndarray, probabilities: np.ndarray, labels: tuple[str, ...] = CLASS_ORDER
) -> float:
    """Mean negative log-likelihood of the observed class under `probabilities`."""
    probabilities = np.clip(np.asarray(probabilities, dtype=float), 1e-15, 1.0)
    actual = _one_hot(results, labels)
    if actual.shape != probabilities.shape:
        raise ValueError("results and probabilities must have matching shape")
    chosen = (probabilities * actual).sum(axis=1)
    return float(-np.log(chosen).mean())


def multiclass_brier_score(
    results: np.ndarray, probabilities: np.ndarray, labels: tuple[str, ...] = CLASS_ORDER
) -> float:
    """Mean squared error between predicted and one-hot outcome vectors."""
    probabilities = np.asarray(probabilities, dtype=float)
    actual = _one_hot(results, labels)
    if actual.shape != probabilities.shape:
        raise ValueError("results and probabilities must have matching shape")
    return float(np.square(probabilities - actual).sum(axis=1).mean())


def accuracy(results: np.ndarray, probabilities: np.ndarray, labels: tuple[str, ...] = CLASS_ORDER) -> float:
    """Share of matches where the most probable class matches the observed result."""
    probabilities = np.asarray(probabilities, dtype=float)
    predicted = np.array(labels)[np.argmax(probabilities, axis=1)]
    return float((predicted == np.asarray(results)).mean())


def goal_mae(actual_goals: np.ndarray, predicted_goals: np.ndarray) -> float:
    """Mean absolute error between actual and expected goal counts."""
    actual_goals = np.asarray(actual_goals, dtype=float)
    predicted_goals = np.asarray(predicted_goals, dtype=float)
    if actual_goals.shape != predicted_goals.shape:
        raise ValueError("actual_goals and predicted_goals must have matching shape")
    return float(np.abs(actual_goals - predicted_goals).mean())


def poisson_negative_log_likelihood(actual_goals: np.ndarray, predicted_rates: np.ndarray) -> float:
    """Mean Poisson NLL of observed goal counts under predicted scoring rates."""
    actual_goals = np.asarray(actual_goals, dtype=float)
    predicted_rates = np.clip(np.asarray(predicted_rates, dtype=float), 1e-9, None)
    if actual_goals.shape != predicted_rates.shape:
        raise ValueError("actual_goals and predicted_rates must have matching shape")
    from scipy.special import gammaln

    nll = predicted_rates - actual_goals * np.log(predicted_rates) + gammaln(actual_goals + 1.0)
    return float(nll.mean())


def calibration_curve(
    results: np.ndarray,
    probabilities: np.ndarray,
    class_index: int,
    n_bins: int = 10,
    labels: tuple[str, ...] = CLASS_ORDER,
) -> dict[str, np.ndarray]:
    """Bin predicted probability for one class and compare to observed frequency.

    Bins with no predictions are dropped rather than reported as NaN.
    """
    probabilities = np.asarray(probabilities, dtype=float)
    actual = _one_hot(results, labels)[:, class_index]
    predicted = probabilities[:, class_index]
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_ids = np.clip(np.digitize(predicted, edges[1:-1], right=True), 0, n_bins - 1)
    mean_predicted, observed_frequency, counts = [], [], []
    for bin_id in range(n_bins):
        mask = bin_ids == bin_id
        count = int(mask.sum())
        if count == 0:
            continue
        mean_predicted.append(float(predicted[mask].mean()))
        observed_frequency.append(float(actual[mask].mean()))
        counts.append(count)
    return {
        "mean_predicted": np.array(mean_predicted),
        "observed_frequency": np.array(observed_frequency),
        "count": np.array(counts, dtype=int),
    }
