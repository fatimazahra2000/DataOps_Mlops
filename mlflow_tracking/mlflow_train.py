import pandas as pd
import numpy as np
import os
import time
import joblib

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# ── Configuration ─────────────────────────────────────
DATA_DIR   = "ML/processed"
MODEL_DIR  = "ML/models"
EXPERIMENT = "film-recommender"
MODEL_NAME = "FilmRecommender"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT)
os.makedirs(MODEL_DIR, exist_ok=True)

# ── Chargement des données ────────────────────────────
print("Chargement des données...")
X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv")).values.ravel()
X_test  = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
y_test  = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv")).values.ravel()

print(f"Train : {X_train.shape} | Test : {X_test.shape}")

# ── Modèles ───────────────────────────────────────────
MODELS = {
    "Ridge_Regression": {
        "pipeline": make_pipeline(
            SimpleImputer(strategy="median"),
            Ridge(alpha=1.0, random_state=42)
        ),
        "params": {"algorithm": "Ridge", "alpha": 1.0, "random_state": 42}
    },
    "Random_Forest": {
        "pipeline": make_pipeline(
            SimpleImputer(strategy="median"),
            RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        ),
        "params": {"algorithm": "RandomForest", "n_estimators": 100, "max_depth": 10, "random_state": 42}
    },
    "Gradient_Boosting": {
        "pipeline": make_pipeline(
            SimpleImputer(strategy="median"),
            GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
        ),
        "params": {"algorithm": "GradientBoosting", "n_estimators": 100, "max_depth": 3, "random_state": 42}
    },
}

# ── Entraînement + Tracking MLflow ───────────────────
results = []

for run_name, config in MODELS.items():
    print(f"\nRun : {run_name}")

    with mlflow.start_run(run_name=run_name):

        mlflow.log_params(config["params"])
        mlflow.log_param("dataset", "MovieLens")
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))

        start = time.time()
        model = config["pipeline"]
        model.fit(X_train, y_train)
        train_time = time.time() - start

        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae  = mean_absolute_error(y_test, y_pred)
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot)

        print(f"  RMSE : {rmse:.4f} | MAE : {mae:.4f} | R² : {r2:.4f}")

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("train_time_sec", train_time)

        local_path = os.path.join(MODEL_DIR, f"{run_name}.pkl")
        joblib.dump(model, local_path)
        mlflow.log_artifact(local_path, artifact_path="joblib_model")

        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn-model",
            registered_model_name=MODEL_NAME,
            serialization_format="cloudpickle",
        )

        run_id = mlflow.active_run().info.run_id
        results.append({
            "run_name": run_name,
            "run_id": run_id,
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        })

# ── Meilleur modèle → Production ─────────────────────
df_results = pd.DataFrame(results).sort_values("rmse")
print(f"\n{'='*50}")
print("RÉSULTATS :")
print(df_results[["run_name", "rmse", "mae", "r2"]].to_string(index=False))

best = df_results.iloc[0]
print(f"\nMeilleur modèle : {best['run_name']} (RMSE = {best['rmse']:.4f})")

client = MlflowClient()
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
best_version = None
for v in versions:
    if v.run_id == best["run_id"]:
        best_version = v.version
        break

if best_version:
    # Ajouter un alias "production" au lieu de stage
    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias="production",
        version=best_version,
    )
    joblib.dump(
        joblib.load(os.path.join(MODEL_DIR, f"{best['run_name']}.pkl")),
        os.path.join(MODEL_DIR, "model.pkl")
    )
    print(f"Modèle v{best_version} ({best['run_name']}) promu en Production ✅")
else:
    print("Avertissement : version introuvable dans le Registry.")

print("\nLance : mlflow ui --port 5000")
print("Puis ouvre : http://localhost:5000")