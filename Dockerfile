FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MATCHCAST_RUNTIME=1
WORKDIR /app
RUN useradd --create-home --uid 10001 matchcast
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN jupyter nbconvert --to script notebooks/07_api_storage.ipynb --output api_runtime --output-dir /app
USER matchcast
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "api_runtime:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
