# Phase 7 — Model Evaluation and Backtesting

**Source:** [`notebooks/05_model_evaluation.ipynb`](../notebooks/05_model_evaluation.ipynb)

## Method

Three expanding-window backtest folds were built on the FIFA World Cup: 2014, 2018,
and 2022 (64 matches each, 192 total). For every fold, the test set is that year's
World Cup matches and the train set is every match strictly before the earliest test
date. Elo pre-match features are already leakage-safe by construction (Phase 4); the
Poisson home/away goal-rate model and the training-frequency reference baseline are
refit from scratch on each fold's train-only data. Split and metric logic live in
`src/matchcast/evaluation/` (`splits.py`, `metrics.py`, `baseline.py`) so every model
is scored identically.

## Per-fold results

| Year | Matches | Baseline log loss | Elo log loss | Poisson log loss | Baseline acc. | Elo acc. | Poisson acc. |
|------|---------|-------------------|---------------|-------------------|----------------|----------|---------------|
| 2014 | 64      | 1.059             | 0.978         | 0.982             | 0.453          | 0.531    | 0.609         |
| 2018 | 64      | 1.094             | 0.971         | 0.995             | 0.391          | 0.563    | 0.563         |
| 2022 | 64      | 1.074             | 1.031         | 1.017             | 0.438          | 0.531    | 0.484         |

Poisson-only goal metrics (expected goals vs. actual):

| Year | Home goal MAE | Away goal MAE | Poisson NLL |
|------|----------------|----------------|-------------|
| 2014 | 0.934          | 1.058          | 1.541       |
| 2018 | 1.067          | 0.743          | 1.433       |
| 2022 | 1.121          | 0.854          | 1.494       |

## Pooled (192 matches)

| Model                        | Log loss | Brier  | Accuracy | Log-loss std across folds |
|-------------------------------|----------|--------|----------|----------------------------|
| Training-frequency baseline   | 1.076    | 0.653  | 0.427    | 0.014                       |
| Elo                            | 0.993    | 0.590  | 0.542    | 0.027                       |
| Poisson                        | 0.998    | 0.594  | 0.552    | 0.015                       |

A reliability plot for pooled home-win probability (Elo vs. Poisson vs. perfect
calibration) is saved at [`reports/phase7_calibration.png`](phase7_calibration.png).

## Decision

Both Elo and Poisson clearly beat the training-frequency baseline on log loss and
Brier score in every fold, confirming both extract real predictive signal rather than
just the unconditional class split. The two are close to each other on outcome
quality (log loss within 0.005 pooled), with Elo's fold-to-fold log loss varying more
(2018 vs. 2022 swing) than Poisson's. **Poisson is selected as the baseline going into
Phase 8** because it matches Elo on outcome probability quality while additionally
producing calibrated scoreline and expected-goals outputs that Elo does not — a
strictly larger deliverable at no observed accuracy cost. Both baselines remain in the
codebase; Phase 8 must beat the Poisson pooled log loss (0.998) on this same harness to
justify a more complex model.

## Limitations

- Only three World Cup folds (192 matches total) are available in the current data
  window; per-fold metrics have visible variance, and the 2022 fold favors Elo on
  accuracy while 2014 favors Poisson, so tournament-level differences should not be
  over-interpreted.
- The training-frequency baseline is refit per fold rather than from one whole-history
  estimate, so its reported probabilities differ slightly across folds by design.
- Calibration bins are coarse (8 bins over 192 pooled matches) because World Cup
  sample sizes are small; a finer-grained calibration check would need a larger
  future-only test set (e.g., qualifiers) at the cost of a less prestige-matched
  backtest.
- Goal MAE and Poisson NLL are only computed for the Poisson model since Elo does not
  produce expected-goal outputs; this is an intentional gap, not a missing metric.
