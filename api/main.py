from fastapi import FastAPI
import pandas as pd
import mlflow.sklearn
import mlflow
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Film Recommender API")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model = None

@app.on_event("startup")
def load_model():
    global model
    model = mlflow.sklearn.load_model("models:/FilmRecommender@production")

@app.get("/health")
def health():
    return {"status": "ok", "model": "FilmRecommender@production", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"prediction": float(prediction[0])}