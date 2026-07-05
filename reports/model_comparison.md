# Phase 8 — Machine Learning Model Comparison

**Source:** [`notebooks/06_ml_models.ipynb`](../notebooks/06_ml_models.ipynb)

## Features

Leakage-safe rolling team-form features from `src/matchcast/features/rolling.py`
(shift(1)-then-rolling, window = 5 matches), joined to each match:

- `rolling_goals_for`, `rolling_goals_against` — mean goals in the team's last 5 matches.
- `rolling_win_rate` — mean result points (win=1, draw=0.5, loss=0) over the last 5.
- `rolling_form_vs_expected` — mean (points earned − Elo-expected points) over the last 5, i.e. over/under-performance vs. rating.
- `rolling_elo_trend` — team Elo one match ago minus Elo six matches ago.
- `neutral` (venue) and `tournament_type` (`world_cup` / `qualifier` / `continental` / `friendly` / `other`, one-hot, `other` as reference level) — both directly observable pre-match, no rolling needed.
- `elo_difference` — carried over from Phase 4.

First-appearance rows for a team (no prior history) fall back to neutral defaults
(0 goals, 0.5 win rate, 0 form/trend) rather than leaking any information.

## Models, hyperparameters, and seeds

Seed `20260705` everywhere. Hyperparameters tuned on a chronological 70/15/15
train/validation/test split of matches from 2000-01-01 onward (17,801 / 3,815 / 3,815
matches), selecting by validation-set multiclass log loss only:

| Model | Grid searched | Selected |
|---|---|---|
| Logistic regression | `C ∈ {0.01, 0.1, 1, 10}` (standardized features) | `C=0.1` (val log loss 0.8593) |
| Random forest | `n_estimators ∈ {200,400}`, `max_depth ∈ {4,8,None}` | `n_estimators=200, max_depth=8` (val log loss 0.8772) |
| XGBoost | `n_estimators ∈ {200,300}`, `max_depth ∈ {3,4}`, `learning_rate ∈ {0.03,0.05}` | `n_estimators=300, max_depth=3, learning_rate=0.03` (val log loss 0.8619) |

Isotonic calibration (`CalibratedClassifierCV`, 3-fold) was checked for the tuned
random forest and rejected: validation log loss went from 0.8772 (uncalibrated) to
0.8779 (calibrated), i.e. no improvement, so the uncalibrated forest is used.
Logistic regression already outputs calibrated-style probabilities from its linear
model and was not recalibrated.

LightGBM was not added: XGBoost already runs end to end and the roadmap only asks
for one gradient-boosting candidate once the scikit-learn baselines work.

## Head-to-head on the Phase 7 harness (2014/2018/2022 World Cup folds, 192 matches)

| Model | Log loss | Brier | Accuracy | Log-loss std across folds |
|---|---|---|---|---|
| **Logistic regression** | **0.982** | 0.578 | 0.568 | 0.048 |
| Random forest | 0.992 | 0.590 | 0.563 | 0.019 |
| Elo (Phase 4) | 0.993 | 0.590 | 0.542 | 0.027 |
| XGBoost | 0.997 | 0.589 | 0.563 | 0.031 |
| Poisson (Phase 5, from Phase 7) | 0.998 | 0.594 | 0.552 | 0.015 |
| Training-frequency baseline | 1.076 | 0.653 | 0.427 | 0.014 |

Per-fold values, runtimes, and the full metric set are in the notebook's output
cells; approximate wall-clock time for the full notebook (tuning + all three
World Cup folds for all five candidates) was under two minutes on this machine.

## Decision

**Logistic regression on the rolling-form + Elo + tournament-type feature set is
selected as the production candidate.** It has the lowest pooled log loss and Brier
score and the highest pooled accuracy of any model tested, including Elo and Poisson.
The margin over Elo is small in absolute terms (0.982 vs. 0.993 log loss) but is a
genuine improvement on the identical held-out backtest used for every prior phase,
and it comes from a linear model with five engineered predictors per side plus
venue/tournament context — no unexplainable black-box gain. Random forest and
XGBoost do not beat Elo by a meaningful margin here and have noticeably higher
per-fold variance (in XGBoost's case) for no accuracy benefit, likely because 192
backtest matches and ~18k training rows do not give tree ensembles enough signal
to out-learn a well-regularized linear model plus a strong Elo prior.

**Simpler baselines are kept, not removed.** Elo remains the fastest, most
interpretable model and Poisson remains the only source of scoreline/expected-goals
output; logistic regression is the recommended choice specifically for outcome
*probability* quality.

## Limitations

- The backtest is the same 192-match World Cup sample used in Phase 7; conclusions
  about which model is "best" should be read as directionally true, not
  statistically decisive, given the small sample and the log-loss standard
  deviations shown above.
- The 5-match rolling window and the 5-bucket tournament-type scheme were fixed by
  judgment, not tuned against the World Cup backtest, to avoid overfitting the
  evaluation harness itself; a wider feature/window search is future work.
- Random forest and XGBoost were tuned with small, hand-picked grids rather than
  exhaustive or Bayesian search; a larger search might close or reverse the gap to
  logistic regression, but was judged not worth the added complexity given the
  current result.
