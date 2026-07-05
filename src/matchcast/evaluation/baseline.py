"""Reference baseline: training-period outcome frequencies only."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from matchcast.evaluation.metrics import CLASS_ORDER


@dataclass(frozen=True)
class TrainingFrequencyBaseline:
    """Predicts the same H/D/A probability vector for every match, fit from training data."""

    probabilities: tuple[float, float, float]

    @classmethod
    def fit(cls, train_results: pd.Series, labels: tuple[str, ...] = CLASS_ORDER) -> "TrainingFrequencyBaseline":
        if len(train_results) == 0:
            raise ValueError("cannot fit a frequency baseline on an empty training set")
        counts = train_results.value_counts()
        total = float(len(train_results))
        probabilities = tuple(float(counts.get(label, 0)) / total for label in labels)
        return cls(probabilities=probabilities)

    def predict(self, n_rows: int) -> np.ndarray:
        return np.tile(np.array(self.probabilities, dtype=float), (n_rows, 1))
