# MatchCast

MatchCast is a backend-first machine learning project for probabilistic
international football prediction, with an initial focus on the 2026 FIFA
World Cup knockout stage.

The project combines data engineering, team-strength ratings, statistical
modelling, probabilistic evaluation, and tournament simulation. It is an
independent portfolio project and is not affiliated with FIFA or any tournament
organizer.

## Current Stage

All local project phases are implemented: reproducible data preparation,
leakage-safe Elo and Poisson baselines, seeded simulation, chronological model
evaluation, a typed API/persistence prototype, and container/CI/MLOps packaging.
The regularized logistic model is selected for outcome probabilities; Poisson
remains the scoreline model. External hosting is intentionally not claimed.

See `docs/reproduction.md`, `docs/api.md`, `docs/model-card.md`, and
`docs/architecture.md`.

## Requirements

- Python 3.10 or newer
- Git
- GNU Make (optional; direct Python commands are also documented)

## Setup

From PowerShell on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

If PowerShell blocks activation scripts, the environment's interpreter can be
used directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
```

## Commands

With the virtual environment activated:

```text
make install    Install dependencies
make test       Run the test suite
make notebook   Start Jupyter Notebook
make data       Download the pinned raw match dataset
make validate-data  Validate raw data and write the JSON report
```

Equivalent commands without GNU Make:

```powershell
python -m pip install -r requirements.txt
python -m pytest
python -m jupyter notebook
python src/matchcast/ingestion/download_results.py
python scripts/validate_data.py
```

## Project Structure

```text
matchcast/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
├── reports/
├── src/
│   └── matchcast/
│       ├── ingestion/
│       ├── features/
│       ├── models/
│       ├── simulation/
│       ├── evaluation/
│       └── api/
├── tests/
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

Raw, interim, and processed data files are ignored by Git by default. Their
directories remain in the repository through `.gitkeep` files.

## Project Rules

- Prediction features must use only information available before kickoff.
- Model evaluation must use chronological splits.
- Reusable code belongs under `src/matchcast/` and requires tests.
- Simple baselines must be evaluated before advanced models are introduced.
- Raw source data must remain unchanged and have documented provenance and
  licensing.

## Licence

See [LICENSE](LICENSE).
