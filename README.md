# MatchCast

MatchCast is a backend-first machine learning project for probabilistic
international football prediction, with an initial focus on the 2026 FIFA
World Cup knockout stage.

The project combines data engineering, team-strength ratings, statistical
modelling, probabilistic evaluation, and tournament simulation. It is an
independent portfolio project and is not affiliated with FIFA or any tournament
organizer.

## Current Stage

The repository foundation is in place. The next active work is acquiring and
validating historical international results and completed 2026 World Cup
matches. The first usable release will prioritize:

1. A reproducible match dataset.
2. A leakage-safe Elo baseline.
3. A Poisson scoreline model.
4. Predictions for remaining knockout fixtures.
5. Monte Carlo simulation of the bracket through the final.

Advanced machine learning, the API, persistence, and deployment follow after
the baseline has been evaluated.

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
```

Equivalent commands without GNU Make:

```powershell
python -m pip install -r requirements.txt
python -m pytest
python -m jupyter notebook
python src/matchcast/ingestion/download_results.py
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
├── TASKS.md
└── matchcast_project_overview_and_roadmap.md
```

Raw, interim, and processed data files are ignored by Git by default. Their
directories remain in the repository through `.gitkeep` files.

## Documentation

- [Task backlog](TASKS.md)
- [Project overview and roadmap](matchcast_project_overview_and_roadmap.md)

## Project Rules

- Prediction features must use only information available before kickoff.
- Model evaluation must use chronological splits.
- Reusable code belongs under `src/matchcast/` and requires tests.
- Simple baselines must be evaluated before advanced models are introduced.
- Raw source data must remain unchanged and have documented provenance and
  licensing.

## Licence

See [LICENSE](LICENSE).
