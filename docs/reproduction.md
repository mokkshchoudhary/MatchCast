# Reproduction Guide

Use Python 3.11. Install with `python -m pip install -r requirements.txt`, then run `python -m pytest`.

Execute notebooks in numeric order with:

```powershell
python -m jupyter nbconvert --to notebook --execute notebooks/07_api_storage.ipynb --output 07_api_storage.ipynb --output-dir notebooks
python -m jupyter nbconvert --to notebook --execute notebooks/08_deployment_mlops.ipynb --output 08_deployment_mlops.ipynb --output-dir notebooks
```

Earlier notebooks reproduce data cleaning, Elo, Poisson, simulation, evaluation, and ML comparisons. Large raw/processed data and generated artifacts are ignored; retrieve/prepare data with the documented ingestion flow. For the service, copy `.env.example` to `.env`, replace the password, then run `docker compose up --build`.

CI installs dependencies, runs tests, executes the service/MLOps notebooks, and builds the container. A missing or version-mismatched model artifact causes startup loading to fail explicitly.
