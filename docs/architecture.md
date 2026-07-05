# MatchCast Architecture

Historical results flow through deterministic cleaning, chronological Elo features, Poisson score modelling, future-only evaluation, and leakage-safe rolling features. The selected logistic model serves outcome probabilities; Poisson serves scorelines; seeded Monte Carlo produces group results.

The FastAPI service is defined and tested in `notebooks/07_api_storage.ipynb`. SQLAlchemy targets PostgreSQL in containers and isolated SQLite during tests. Predictions and simulations persist input metadata and model versions. API and database run as separate Compose services. JSON request logs and `/metrics` provide basic observability.

No queue is currently justified: simulations are bounded and synchronous. A worker/queue boundary can be added behind the existing simulation resource if measured latency exceeds the service objective.
