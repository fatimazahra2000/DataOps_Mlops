import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# ── Configuration ────────────────────────────────────────────────────────────
DATA_DIR        = "ML/processed"
MODEL_NAME      = "FilmRecommender"
EXPERIMENT_MON  = "film-recommender-monitoring"
DRIFT_THRESHOLD = 0.10

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_MON)

client = MlflowClient()

# ── 1. Récupérer le modèle en Production ─────────────────────────────────────
print("Récupération du modèle en Production...")

try:
    model_uri = f"models:/{MODEL_NAME}@production"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Modèle chargé depuis Registry : {model_uri}")
    baseline_rmse = None

    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    for v in versions:
        if v.aliases and "production" in v.aliases:
            run = client.get_run(v.run_id)
            baseline_rmse = run.data.metrics.get("rmse", None)
            baseline_algo = run.data.params.get("algorithm", "inconnu")
            prod_version = v.version
            break

except Exception as e:
    print(f"Erreur Registry : {e}")
    model = joblib.load("ML/models/model.pkl")
    baseline_rmse = None
    prod_version = "local"
    baseline_algo = "GradientBoosting"

# ── 2. Recalculer les métriques ───────────────────────────────────────────────
print("Chargement des données de test...")
X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv")).values.ravel()

y_pred = model.predict(X_test)
current_rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
current_mae  = np.mean(np.abs(y_test - y_pred))
ss_res = np.sum((y_test - y_pred) ** 2)
ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
current_r2 = 1 - (ss_res / ss_tot)

print(f"RMSE : {current_rmse:.4f} | MAE : {current_mae:.4f} | R² : {current_r2:.4f}")

# ── 3. Détection de dérive ────────────────────────────────────────────────────
drift_detected = False
drift_pct      = 0.0

if baseline_rmse is not None:
    drift_pct      = (current_rmse - baseline_rmse) / baseline_rmse
    drift_detected = drift_pct > DRIFT_THRESHOLD
    if drift_detected:
        print(f"⚠️  DRIFT DÉTECTÉ : {drift_pct*100:+.2f}%")
    else:
        print(f"✅ Modèle stable : dérive = {drift_pct*100:+.2f}%")

# ── 4. Logger dans MLflow ─────────────────────────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

with mlflow.start_run(run_name=f"monitoring_{timestamp}"):
    mlflow.set_tag("type", "monitoring")
    mlflow.log_metric("current_rmse", current_rmse)
    mlflow.log_metric("current_mae",  current_mae)
    mlflow.log_metric("current_r2",   current_r2)
    if baseline_rmse:
        mlflow.log_metric("baseline_rmse", baseline_rmse)
        mlflow.log_metric("drift_pct", drift_pct * 100)
        mlflow.log_param("drift_alert", str(drift_detected))

print(f"Run de monitoring loggé ✅")

# ── 5. Rapport ────────────────────────────────────────────────────────────────
os.makedirs("monitoring/reports", exist_ok=True)
report = f"""
========================================
RAPPORT DE MONITORING — {timestamp}
========================================
RMSE actuel  : {current_rmse:.4f}
MAE actuel   : {current_mae:.4f}
R² actuel    : {current_r2:.4f}
Baseline     : {baseline_rmse if baseline_rmse else 'N/A'}
Dérive       : {f'{drift_pct*100:+.2f}%' if baseline_rmse else 'N/A'}
Alerte       : {'OUI ⚠️' if drift_detected else 'NON ✅'}
========================================
"""
print(report)
with open(f"monitoring/reports/report_{timestamp}.txt", "w") as f:
    f.write(report)