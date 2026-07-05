# MatchCast Portfolio Material

## Project narrative

MatchCast is a leakage-safe international-football prediction system built from raw-result validation through chronological Elo and Poisson baselines, calibrated model comparison, reproducible Monte Carlo simulation, and a versioned FastAPI/PostgreSQL deployment design. The main engineering result is not a single prediction: it is a reproducible evidence chain showing why a regularized linear model was selected.

## Resume bullets

- Built a chronological football prediction pipeline over 49k international matches, preventing pre-kickoff feature leakage and comparing Elo, Poisson, logistic regression, random forest, and XGBoost on identical World Cup folds.
- Improved pooled multiclass log loss from 0.993 (Elo) to 0.982 with leakage-safe rolling features and a regularized logistic model; retained Poisson for normalized scoreline distributions.
- Designed a typed FastAPI/PostgreSQL service with versioned prediction persistence, seeded tournament simulation, structured errors/logs, metrics, Docker Compose, CI, and MLflow experiment metadata.

## LinkedIn milestones

1. Data and Elo: explain provenance, chronological updates, and why leakage prevention matters.
2. Probabilistic modelling: show Poisson score matrices and seeded qualification probabilities.
3. Evaluation: publish the identical-fold comparison and the decision to prefer a simpler linear model.
4. Productization: show OpenAPI, persistence schema, container health checks, CI, and the model card.

Suggested screenshots: Phase 7 calibration chart, Phase 8 comparison table, `/docs`, and the Phase 6 qualification table. Do not imply external production deployment unless one is actually maintained.
