# MatchCast Task Backlog

This file is the executable project tracker for the vision described in
[`matchcast_project_overview_and_roadmap.md`](matchcast_project_overview_and_roadmap.md).

## Status Legend

- `[x]` Completed and verified in the repository
- `[ ]` Pending

## Project Principles

- Implement backlog tasks as self-contained Jupyter notebooks under `notebooks/`, not as new `.py` files.
- Include executable validation checks in each notebook and run them before marking the task complete.
- Use only information available before a match when generating prediction features.
- Establish and evaluate simple baselines before introducing advanced models.
- Split training and evaluation data chronologically; never use random splits for backtests.
- Record model configuration, data boundaries, metrics, and reproducibility information.
- Keep raw source data immutable and document its origin and licence.

## Task Completion Workflow

Every task must follow this workflow before it is marked complete:

1. Implement the task in a notebook and run its embedded validation checks.
2. Update the task checkbox to `[x]` only after the validation succeeds.
3. Commit the task's code and documentation with a focused commit message.
4. Push the commit to the remote `main` branch.

A task is not complete until its commit has been pushed successfully to `main`.

## Phase 1: Project Setup and Direction

**Objective:** Establish a reproducible Python repository with a clear project identity and working developer commands.

**Dependencies:** None.

### Tasks

- [x] 1. Create `data/raw/`, `data/interim/`, and `data/processed/`.
- [x] 2. Create `notebooks/`, `reports/`, `tests/`, and the `src/` layout.
- [x] 3. Create the `src/matchcast/` package and its `ingestion`, `features`, `models`, `simulation`, `evaluation`, and `api` subpackages.
- [x] 4. Add `README.md`, `requirements.txt`, `pyproject.toml`, `Makefile`, `.gitignore`, and `LICENSE`.
- [x] 5. Create a local Python virtual environment.
- [x] 6. Document the MatchCast project vision and roadmap.
- [x] 7. Verify a clean environment can install all dependencies from the declared project files.
- [x] 8. Verify the Makefile install, test, and notebook commands on Windows.
- [x] 9. Review README formatting, setup instructions, commands, and project-tree accuracy.
- [x] 10. Confirm generated files, environments, notebook checkpoints, caches, data outputs, and model artifacts are ignored appropriately.
- [x] 11. Run the initial test command successfully, even if the suite initially contains only a smoke test.
- [x] 12. Commit the verified initial project setup.

### Deliverables

- Reproducible repository skeleton.
- Working local environment and developer commands.
- Accurate README, roadmap, and task backlog.

### Definition of Done

Phase 1 is complete when a fresh checkout can be installed, imported, and tested using documented commands, and the verified setup is committed.

## Phase 2: Data Collection — Next Active Phase

**Objective:** Acquire a reliable, documented dataset of historical senior international football results.

**Dependencies:** Verified Phase 1 environment.

### Tasks

- [x] 1. Define the minimum match schema: `date`, `home_team`, `away_team`, `home_score`, `away_score`, `tournament`, `city`, `country`, and `neutral`.
- [x] 2. Compare candidate datasets for coverage, update frequency, provenance, licence, schema quality, and stable access.
- [x] 3. Select the initial dataset and record the source URL, retrieval method, retrieval date, licence, and known limitations.
- [x] 4. Add a reproducible ingestion or download command under `src/matchcast/ingestion/`.
- [x] 5. Store the untouched source file in `data/raw/` without manual edits.
- [x] 6. Validate required columns, parseable dates, non-negative scores, valid neutral flags, and non-empty team names.
- [x] 7. Produce a machine-readable validation summary with row count, date range, missing values, and rejected rows.
- [x] 8. Add ingestion tests using a small committed fixture rather than the full dataset.
- [x] 9. Document how to refresh the raw data without overwriting provenance information.
- [x] 10. Commit source metadata and code; keep large or restricted raw files out of Git when required by licence or repository policy.

### Deliverables

- Documented raw match dataset in `data/raw/`.
- Reproducible ingestion code and validation report.
- Automated ingestion tests.

### Definition of Done

Phase 2 is complete when another developer can retrieve the same source, validate its schema, understand its licence and limitations, and reproduce the raw-data state.

## Phase 3: Data Cleaning and Exploration — Complete

**Objective:** Produce a consistent, leakage-safe match table and document its important characteristics.

**Dependencies:** Validated Phase 2 raw dataset.

### Tasks

- [x] 1. Define the processed match schema and data types.
- [x] 2. Parse and sort match dates deterministically.
- [x] 3. Normalize whitespace, casing, and known aliases in team names using an explicit mapping.
- [x] 4. Preserve original team names or source identifiers for traceability.
- [x] 5. Handle missing, duplicate, malformed, and impossible records with documented rules.
- [x] 6. Add `result` and `goal_difference` fields.
- [x] 7. Save the cleaned table under `data/processed/` through a reproducible command.
- [x] 8. Create `notebooks/01_data_exploration.ipynb`.
- [x] 9. Report match count, date range, team count, matches by year, most active teams, average goals, outcome distribution, common scorelines, and missing values.
- [x] 10. Add tests for cleaning rules, derived fields, duplicate handling, and deterministic output.
- [x] 11. Document data-quality findings and remaining limitations.

### Deliverables

- Reproducible processed match dataset.
- Data exploration notebook and quality summary.
- Cleaning tests.

### Definition of Done

Phase 3 is complete when processing the raw data produces a deterministic, validated table and the notebook answers every exploration question in the roadmap.

## Phase 4: Elo Rating Baseline — Complete

**Objective:** Build the first chronological team-strength and outcome-probability baseline.

**Dependencies:** Chronologically sorted Phase 3 match data.

### Tasks

- [x] 1. Specify initial rating, K-factor, home advantage, neutral-venue behavior, and update formula.
- [x] 2. Implement Elo calculations in the self-contained `notebooks/02_elo_baseline.ipynb` (not a new `.py` file, per repository instructions).
- [x] 3. Store pre-match home Elo, away Elo, and Elo difference for every match.
- [x] 4. Update ratings only after recording the features for that match.
- [x] 5. Convert rating differences into home/draw/away probabilities using a documented baseline method.
- [x] 6. Define deterministic handling for same-day matches and previously unseen teams.
- [x] 7. Add embedded validation checks for expected score, rating updates, neutral venues, new teams, and chronological leakage prevention.
- [x] 8. Create `notebooks/02_elo_baseline.ipynb`.
- [x] 9. Report baseline predictions and preliminary probabilistic metrics on a chronological holdout.

### Deliverables

- Reusable Elo feature module.
- Match-level pre-match Elo features.
- Baseline notebook and tests.

### Definition of Done

Phase 4 is complete when Elo features are reproducible, use no future information, pass leakage tests, and generate valid probabilities summing to one.

## Phase 5: Poisson Scoreline Model

**Objective:** Estimate expected goals and coherent exact-score and match-outcome probabilities.

**Dependencies:** Phase 3 data and Phase 4 strength features.

### Tasks

- [x] 1. Define the training window, predictors, home effect, regularization approach, and maximum displayed score.
- [x] 2. Implement the model in the self-contained `notebooks/03_poisson_model.ipynb` (not a new `.py` file, per repository instructions).
- [x] 3. Fit separate home- and away-goal expectations using training-period data only.
- [x] 4. Generate an exact-score probability matrix and account for truncated tail probability.
- [x] 5. Derive home-win, draw, away-win, most-likely-score, and expected-goals outputs.
- [x] 6. Validate that probabilities are non-negative, finite, and normalized.
- [x] 7. Add embedded checks for Poisson probabilities, score-matrix aggregation, truncation handling, and deterministic predictions.
- [x] 8. Create and execute `notebooks/03_poisson_model.ipynb`.
- [x] 9. Compare Poisson outcome probabilities with the Elo baseline on the same chronological holdout.

### Deliverables

- Reusable Poisson model.
- Scoreline and outcome prediction outputs.
- Comparison notebook and tests.

### Definition of Done

Phase 5 is complete when the model produces validated score and outcome distributions for unseen matches and can be compared fairly with Elo.

## Phase 6: Match and Group Simulation

**Objective:** Turn model probabilities into reproducible match and group-stage simulations.

**Dependencies:** Validated Phase 5 scoreline distributions.

### Tasks

- [x] 1. Define typed inputs and outputs for match and group simulation.
- [x] 2. Implement seeded match-score sampling in the self-contained simulation notebook (not a new `.py` file, per repository instructions).
- [x] 3. Aggregate repeated simulations into scoreline and outcome frequencies.
- [x] 4. Implement round-robin fixture generation for a small group.
- [x] 5. Calculate points, goal difference, goals scored, and deterministic standings.
- [x] 6. Define and document the supported tie-break order and unresolved-tie fallback.
- [x] 7. Estimate qualification and finishing-position probabilities across Monte Carlo runs.
- [x] 8. Add embedded checks for seeding, standings arithmetic, tie-breaks, probability totals, and repeatability.
- [x] 9. Create and execute `notebooks/04_simulation_baseline.ipynb`.
- [x] 10. Produce a readable simulation report under `reports/`.

### Deliverables

- Match and group simulation modules.
- Simulation notebook and report.
- Deterministic automated tests.

### Definition of Done

Phase 6 is complete when seeded runs are reproducible, standings rules are tested, and aggregate qualification probabilities are valid.

## Phase 7: Model Evaluation and Backtesting

**Objective:** Measure predictive performance and calibration on future matches.

**Dependencies:** Elo, Poisson, and simulation baselines from Phases 4–6.

### Tasks

- [ ] 1. Define chronological train, validation, and tournament backtest boundaries.
- [ ] 2. Implement multiclass log loss, Brier score, calibration analysis, goal MAE, and Poisson negative log-likelihood under `src/matchcast/evaluation/`.
- [ ] 3. Add a simple reference baseline based on training-period outcome frequencies.
- [ ] 4. Run expanding-window backtests for the 2014, 2018, and 2022 World Cups when dataset coverage permits.
- [ ] 5. Ensure all preprocessing, Elo state, and fitted model parameters use training-period data only.
- [ ] 6. Report per-fold and aggregate metrics with sample counts and uncertainty where practical.
- [ ] 7. Plot calibration and compare every model against the reference baseline.
- [ ] 8. Add tests for metric calculations, split boundaries, and leakage guards.
- [ ] 9. Write `reports/model_evaluation.md` with results, limitations, and a model-selection decision.

### Deliverables

- Reusable evaluation package.
- Reproducible chronological backtests.
- Model evaluation report.

### Definition of Done

Phase 7 is complete when baselines are compared on identical future-only folds and the selected model is justified by probabilistic metrics and calibration.

## Phase 8: Machine Learning Models

**Objective:** Test whether engineered features improve on evaluated statistical baselines.

**Dependencies:** Phase 7 evaluation harness and accepted baseline.

### Tasks

- [ ] 1. Implement leakage-safe rolling features for recent goals, goals conceded, win rate, opponent-adjusted form, neutral venue, tournament type, and rating trend.
- [ ] 2. Add chronological feature-generation tests with explicit cutoff assertions.
- [ ] 3. Build a reproducible logistic-regression baseline.
- [ ] 4. Build and tune a tree-based candidate such as random forest.
- [ ] 5. Add XGBoost or LightGBM only after the scikit-learn baselines run end to end.
- [ ] 6. Tune models using chronological validation rather than the final test periods.
- [ ] 7. Calibrate candidate probabilities when validation evidence supports it.
- [ ] 8. Compare all candidates through the Phase 7 evaluation harness.
- [ ] 9. Record feature definitions, hyperparameters, seeds, runtime, and metrics.
- [ ] 10. Write `reports/model_comparison.md` and select a production candidate without removing simpler baselines.

### Deliverables

- Leakage-safe feature pipeline.
- Reproducible ML training pipelines.
- Model comparison report.

### Definition of Done

Phase 8 is complete when each model is evaluated on identical chronological folds and any claimed improvement is supported by reproducible metrics.

## Phase 9: Backend API and Storage

**Objective:** Expose versioned prediction and simulation behavior through a validated backend service with persistence.

**Dependencies:** Selected model and stable prediction interfaces from Phases 7–8.

### Tasks

- [ ] 1. Define request, response, error, model-version, and probability schemas.
- [ ] 2. Implement `GET /health` and `GET /teams`.
- [ ] 3. Implement `POST /predict-match`.
- [ ] 4. Implement `POST /simulate-tournament`.
- [ ] 5. Implement `GET /simulation/{simulation_id}`.
- [ ] 6. Implement `GET /models/leaderboard`.
- [ ] 7. Validate unknown teams, invalid fixtures, unsupported formats, and simulation limits.
- [ ] 8. Add structured logging and consistent error responses without leaking internal details.
- [ ] 9. Define PostgreSQL tables for teams, matches, model versions, predictions, simulations, and simulation results.
- [ ] 10. Add SQLAlchemy models, database configuration, and migrations.
- [ ] 11. Persist model version and input metadata with every prediction and simulation.
- [ ] 12. Add API unit and integration tests, including database rollback or isolated test storage.
- [ ] 13. Document local API and database startup and provide example requests.

### Deliverables

- FastAPI service under `src/matchcast/api/`.
- PostgreSQL persistence and migrations.
- Tested API documentation.

### Definition of Done

Phase 9 is complete when documented endpoints validate inputs, return reproducible versioned outputs, persist required records, and pass automated API and database tests.

## Phase 10: Deployment, MLOps, and Portfolio Packaging

**Objective:** Make MatchCast reproducible, observable, automated, and suitable for public portfolio review.

**Dependencies:** Tested Phase 9 service.

### Tasks

- [ ] 1. Add a production-oriented application Dockerfile.
- [ ] 2. Add Docker Compose for the API and PostgreSQL with health checks and persistent local storage.
- [ ] 3. Add GitHub Actions for installation, linting, tests, and build verification.
- [ ] 4. Add environment-based configuration and document required variables without committing secrets.
- [ ] 5. Add MLflow experiment tracking for model parameters, metrics, artifacts, and data/version references.
- [ ] 6. Add model serialization, loading, versioning, and startup-failure behavior.
- [ ] 7. Add model cards describing training data, evaluation, intended use, limitations, and ethical considerations.
- [ ] 8. Add operational logging and basic service metrics.
- [ ] 9. Add a PyTorch model only as a measured extension through the same evaluation harness.
- [ ] 10. Add player embeddings and attention pooling only after reliable player and squad data are available.
- [ ] 11. Add asynchronous simulation jobs only when measured request latency or workload requires them.
- [ ] 12. Complete architecture, data, model, API, deployment, and reproduction documentation.
- [ ] 13. Prepare LinkedIn milestone posts, resume bullets, screenshots, and a concise final project narrative.
- [ ] 14. Run a clean-checkout reproduction test for data preparation, training, evaluation, API startup, and tests.
- [ ] 15. Optionally deploy the backend and document its environment, limitations, and maintenance status.

### Deliverables

- Containerized and automated MatchCast system.
- Tracked experiments, versioned model artifacts, and model cards.
- Portfolio-ready repository and supporting content.

### Definition of Done

Phase 10 is complete when a clean checkout passes CI, runs through documented container commands, reproduces the selected model evidence, and clearly communicates the system's design and limitations.

## Final Milestone Checklist

- [ ] **Data:** Raw data provenance, validation, cleaning, and processed outputs are reproducible.
- [x] **Elo:** Pre-match team ratings and valid outcome probabilities are generated without leakage.
- [ ] **Poisson:** Expected goals, scorelines, and outcome distributions are validated.
- [ ] **Simulation:** Seeded match and group simulations produce tested standings and qualification probabilities.
- [ ] **Evaluation:** Models are compared through future-only backtests using probabilistic metrics and calibration.
- [ ] **Machine learning:** Any advanced model demonstrates reproducible value over the accepted baselines.
- [ ] **API:** Prediction, simulation, health, team, and model endpoints are documented and tested.
- [ ] **Persistence:** PostgreSQL stores versioned inputs, predictions, and simulation results through migrations.
- [ ] **Deployment:** Containers and CI reproduce installation, tests, builds, and service startup.
- [ ] **MLOps:** Experiments and model artifacts are tracked with sufficient data and configuration metadata.
- [ ] **Portfolio:** README, reports, model cards, architecture documentation, posts, and resume material tell one accurate project story.

## Backlog Maintenance

- Update a checkbox only after its repository evidence or documented external deliverable exists.
- Commit and push each completed task to `main` before starting the next task.
- Add newly discovered work to the relevant phase rather than bypassing dependencies.
- Record major scope or architecture decisions in the roadmap or a dedicated decision record.
- Keep implementation details in code and focused documentation; keep this file centered on outcomes and verification.
