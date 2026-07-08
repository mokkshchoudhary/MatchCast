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

The historical pre-tournament audit in
`notebooks/09_world_cup_2010_2022_backtest.ipynb` freezes predictions before
revealing actual results for all 256 matches in the 2010–2022 World Cups.

## 2026 World Cup Results vs Predictions

`notebooks/13_world_cup_2026_results_vs_predictions.ipynb` audits every 2026
FIFA World Cup match currently present in the local processed dataset. For each
match date, the selected weighted logistic model is trained only on matches
before that date, then compared with the actual result.

Local 2026 World Cup audit through 2026-07-03: 55/88 correct (62.50%).

| Date | Match | Score | Model pick | Actual | Correct |
| --- | --- | --- | --- | --- | --- |
| 2026-06-11 | Mexico vs South Africa | 2-0 | Mexico | Mexico | Yes |
| 2026-06-11 | South Korea vs Czech Republic | 2-1 | South Korea | South Korea | Yes |
| 2026-06-12 | Canada vs Bosnia and Herzegovina | 1-1 | Canada | Draw | No |
| 2026-06-12 | United States vs Paraguay | 4-1 | Paraguay | United States | No |
| 2026-06-13 | Qatar vs Switzerland | 1-1 | Switzerland | Draw | No |
| 2026-06-13 | Brazil vs Morocco | 1-1 | Brazil | Draw | No |
| 2026-06-13 | Haiti vs Scotland | 0-1 | Scotland | Scotland | Yes |
| 2026-06-13 | Australia vs Turkey | 2-0 | Turkey | Australia | No |
| 2026-06-14 | Germany vs CuraÃ§ao | 7-1 | Germany | Germany | Yes |
| 2026-06-14 | Ivory Coast vs Ecuador | 1-0 | Ecuador | Ivory Coast | No |
| 2026-06-14 | Netherlands vs Japan | 2-2 | Japan | Draw | No |
| 2026-06-14 | Sweden vs Tunisia | 5-1 | Tunisia | Sweden | No |
| 2026-06-15 | Belgium vs Egypt | 1-1 | Belgium | Draw | No |
| 2026-06-15 | Iran vs New Zealand | 2-2 | Iran | Draw | No |
| 2026-06-15 | Spain vs Cape Verde | 0-0 | Spain | Draw | No |
| 2026-06-15 | Saudi Arabia vs Uruguay | 1-1 | Uruguay | Draw | No |
| 2026-06-16 | France vs Senegal | 3-1 | France | France | Yes |
| 2026-06-16 | Iraq vs Norway | 1-4 | Norway | Norway | Yes |
| 2026-06-16 | Argentina vs Algeria | 3-0 | Argentina | Argentina | Yes |
| 2026-06-16 | Austria vs Jordan | 3-1 | Austria | Austria | Yes |
| 2026-06-17 | Portugal vs DR Congo | 1-1 | Portugal | Draw | No |
| 2026-06-17 | Uzbekistan vs Colombia | 1-3 | Colombia | Colombia | Yes |
| 2026-06-17 | England vs Croatia | 4-2 | England | England | Yes |
| 2026-06-17 | Ghana vs Panama | 1-0 | Panama | Ghana | No |
| 2026-06-18 | Czech Republic vs South Africa | 1-1 | Czech Republic | Draw | No |
| 2026-06-18 | Mexico vs South Korea | 1-0 | Mexico | Mexico | Yes |
| 2026-06-18 | Switzerland vs Bosnia and Herzegovina | 4-1 | Switzerland | Switzerland | Yes |
| 2026-06-18 | Canada vs Qatar | 6-0 | Canada | Canada | Yes |
| 2026-06-19 | Scotland vs Morocco | 0-1 | Morocco | Morocco | Yes |
| 2026-06-19 | Brazil vs Haiti | 3-0 | Brazil | Brazil | Yes |
| 2026-06-19 | United States vs Australia | 2-0 | United States | United States | Yes |
| 2026-06-19 | Turkey vs Paraguay | 0-1 | Turkey | Paraguay | No |
| 2026-06-20 | Germany vs Ivory Coast | 2-1 | Germany | Germany | Yes |
| 2026-06-20 | Ecuador vs CuraÃ§ao | 0-0 | Ecuador | Draw | No |
| 2026-06-20 | Netherlands vs Sweden | 5-1 | Netherlands | Netherlands | Yes |
| 2026-06-20 | Tunisia vs Japan | 0-4 | Japan | Japan | Yes |
| 2026-06-21 | Belgium vs Iran | 0-0 | Belgium | Draw | No |
| 2026-06-21 | New Zealand vs Egypt | 1-3 | Egypt | Egypt | Yes |
| 2026-06-21 | Spain vs Saudi Arabia | 4-0 | Spain | Spain | Yes |
| 2026-06-21 | Uruguay vs Cape Verde | 2-2 | Uruguay | Draw | No |
| 2026-06-22 | France vs Iraq | 3-0 | France | France | Yes |
| 2026-06-22 | Norway vs Senegal | 3-2 | Norway | Norway | Yes |
| 2026-06-22 | Argentina vs Austria | 2-0 | Argentina | Argentina | Yes |
| 2026-06-22 | Jordan vs Algeria | 1-2 | Algeria | Algeria | Yes |
| 2026-06-23 | Portugal vs Uzbekistan | 5-0 | Portugal | Portugal | Yes |
| 2026-06-23 | Colombia vs DR Congo | 1-0 | Colombia | Colombia | Yes |
| 2026-06-23 | England vs Ghana | 0-0 | England | Draw | No |
| 2026-06-23 | Panama vs Croatia | 0-1 | Croatia | Croatia | Yes |
| 2026-06-24 | Mexico vs Czech Republic | 3-0 | Mexico | Mexico | Yes |
| 2026-06-24 | South Africa vs South Korea | 1-0 | South Korea | South Africa | No |
| 2026-06-24 | Canada vs Switzerland | 1-2 | Canada | Switzerland | No |
| 2026-06-24 | Bosnia and Herzegovina vs Qatar | 3-1 | Bosnia and Herzegovina | Bosnia and Herzegovina | Yes |
| 2026-06-24 | Scotland vs Brazil | 0-3 | Brazil | Brazil | Yes |
| 2026-06-24 | Morocco vs Haiti | 4-2 | Morocco | Morocco | Yes |
| 2026-06-25 | United States vs Turkey | 2-3 | United States | Turkey | No |
| 2026-06-25 | Paraguay vs Australia | 0-0 | Paraguay | Draw | No |
| 2026-06-25 | CuraÃ§ao vs Ivory Coast | 0-2 | Ivory Coast | Ivory Coast | Yes |
| 2026-06-25 | Ecuador vs Germany | 2-1 | Ecuador | Ecuador | Yes |
| 2026-06-25 | Japan vs Sweden | 1-1 | Japan | Draw | No |
| 2026-06-25 | Tunisia vs Netherlands | 1-3 | Netherlands | Netherlands | Yes |
| 2026-06-26 | Egypt vs Iran | 1-1 | Egypt | Draw | No |
| 2026-06-26 | New Zealand vs Belgium | 1-5 | Belgium | Belgium | Yes |
| 2026-06-26 | Cape Verde vs Saudi Arabia | 0-0 | Cape Verde | Draw | No |
| 2026-06-26 | Uruguay vs Spain | 0-1 | Spain | Spain | Yes |
| 2026-06-26 | Norway vs France | 1-4 | France | France | Yes |
| 2026-06-26 | Senegal vs Iraq | 5-0 | Senegal | Senegal | Yes |
| 2026-06-27 | Algeria vs Austria | 3-3 | Algeria | Draw | No |
| 2026-06-27 | Jordan vs Argentina | 1-3 | Argentina | Argentina | Yes |
| 2026-06-27 | Colombia vs Portugal | 0-0 | Colombia | Draw | No |
| 2026-06-27 | DR Congo vs Uzbekistan | 3-1 | DR Congo | DR Congo | Yes |
| 2026-06-27 | Panama vs England | 0-2 | England | England | Yes |
| 2026-06-27 | Croatia vs Ghana | 2-1 | Croatia | Croatia | Yes |
| 2026-06-28 | South Africa vs Canada | 0-1 | Canada | Canada | Yes |
| 2026-06-29 | Brazil vs Japan | 2-1 | Brazil | Brazil | Yes |
| 2026-06-29 | Germany vs Paraguay | 1-1 | Germany | Draw | No |
| 2026-06-29 | Netherlands vs Morocco | 1-1 | Netherlands | Draw | No |
| 2026-06-30 | Ivory Coast vs Norway | 1-2 | Ivory Coast | Norway | No |
| 2026-06-30 | France vs Sweden | 3-0 | France | France | Yes |
| 2026-06-30 | Mexico vs Ecuador | 2-0 | Mexico | Mexico | Yes |
| 2026-07-01 | England vs DR Congo | 2-1 | England | England | Yes |
| 2026-07-01 | Belgium vs Senegal | 3-2 | Belgium | Belgium | Yes |
| 2026-07-01 | United States vs Bosnia and Herzegovina | 2-0 | United States | United States | Yes |
| 2026-07-02 | Spain vs Austria | 3-0 | Spain | Spain | Yes |
| 2026-07-02 | Portugal vs Croatia | 2-1 | Portugal | Portugal | Yes |
| 2026-07-02 | Switzerland vs Algeria | 2-0 | Switzerland | Switzerland | Yes |
| 2026-07-03 | Australia vs Egypt | 1-1 | Australia | Draw | No |
| 2026-07-03 | Argentina vs Cape Verde | 3-2 | Argentina | Argentina | Yes |
| 2026-07-03 | Colombia vs Ghana | 1-0 | Colombia | Colombia | Yes |

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
