install:
	pip install -r requirements.txt

test:
	pytest

notebook:
	jupyter notebook

data:
	python src/matchcast/ingestion/download_results.py
