FROM python:3.11-slim

WORKDIR /app

COPY api/requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY api/ ./api/
COPY mlflow_tracking/ ./mlflow_tracking/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]