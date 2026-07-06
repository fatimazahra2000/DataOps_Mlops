"""
mlflow_utils.py — Hafsa (MLOps Engineer)
==========================================
Fonctions utilitaires MLflow réutilisables
par toute l'équipe (Jihad, Amina, etc.)
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import joblib
import os

import os
from dotenv import load_dotenv
load_dotenv()
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MODEL_NAME   = "FilmRecommender"

def setup_mlflow(experiment_name: str = "film-recommender"):
    """Configure MLflow et crée l'expérience si elle n'existe pas."""
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(experiment_name)
    print(f"MLflow configuré — Expérience : {experiment_name}")

def log_model_run(model, run_name: str, params: dict, metrics: dict, model_dir: str = "ML/models"):
    """
    Logge un run MLflow complet :
    paramètres + métriques + modèle + artefact joblib.
    
    Usage :
        log_model_run(model, "GradientBoosting",
                      params={"n_estimators": 100},
                      metrics={"rmse": 0.948})
    """
    os.makedirs(model_dir, exist_ok=True)

    with mlflow.start_run(run_name=run_name):
        # Paramètres
        mlflow.log_params(params)

        # Métriques
        mlflow.log_metrics(metrics)

        # Sauvegarde joblib locale
        local_path = os.path.join(model_dir, f"{run_name}.pkl")
        joblib.dump(model, local_path)
        mlflow.log_artifact(local_path, artifact_path="joblib_model")

        # Enregistrement dans le Registry
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn-model",
            registered_model_name=MODEL_NAME,
            serialization_format="cloudpickle",
        )

        run_id = mlflow.active_run().info.run_id
        print(f"Run loggé : {run_name} | run_id={run_id}")
        return run_id

def get_best_run(experiment_name: str = "film-recommender", metric: str = "rmse"):
    """Retourne le run avec la meilleure métrique (la plus basse par défaut)."""
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if not experiment:
        print(f"Expérience '{experiment_name}' introuvable.")
        return None
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} ASC"],
        max_results=1,
    )
    if not runs:
        return None
    best = runs[0]
    print(f"Meilleur run : {best.data.tags.get('mlflow.runName', best.info.run_id)}")
    print(f"  {metric} = {best.data.metrics.get(metric)}")
    return best

def promote_to_production(run_id: str):
    """Promeut le modèle correspondant au run_id en @production."""
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    for v in versions:
        if v.run_id == run_id:
            client.set_registered_model_alias(
                name=MODEL_NAME,
                alias="production",
                version=v.version,
            )
            print(f"Modèle v{v.version} promu en @production ✅")
            return v.version
    print("Version introuvable pour ce run_id.")
    return None

def load_production_model():
    """Charge le modèle actuellement en @production depuis le Registry."""
    mlflow.set_tracking_uri(TRACKING_URI)
    model_uri = f"models:/{MODEL_NAME}@production"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Modèle chargé depuis : {model_uri}")
    return model

def get_production_metrics():
    """Retourne les métriques du modèle actuellement en @production."""
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    for v in versions:
        if v.aliases and "production" in v.aliases:
            run = client.get_run(v.run_id)
            metrics = run.data.metrics
            params  = run.data.params
            print(f"Modèle en production : v{v.version}")
            print(f"  RMSE : {metrics.get('rmse', 'N/A')}")
            print(f"  MAE  : {metrics.get('mae', 'N/A')}")
            print(f"  R²   : {metrics.get('r2', 'N/A')}")
            return metrics, params
    print("Aucun modèle en @production trouvé.")
    return None, None