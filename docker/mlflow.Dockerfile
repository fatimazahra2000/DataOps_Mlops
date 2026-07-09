FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow

EXPOSE 5000

CMD mlflow server --host 0.0.0.0 --port $PORT \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /app/mlartifacts