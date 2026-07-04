install:
	pip install -r requirements.txt

test:
	pytest

notebook:
	jupyter notebook

data:
	python src/matchcast/ingestion/download_results.py

validate-data:
	python scripts/validate_data.py
