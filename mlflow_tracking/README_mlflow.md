# MLflow Tracking — FilmRecommender

**Responsable : Elhilali Hafsa — MLOps Engineer**

## Vue d'ensemble

Ce dossier contient les scripts MLflow pour le tracking des expériences,
la gestion du registre de modèles et le monitoring des performances.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `mlflow_train.py` | Lance 3 runs, logge paramètres + métriques, promeut le meilleur modèle |
| `mlflow_utils.py` | Fonctions utilitaires réutilisables par toute l'équipe |

## Installation

```bash
pip install mlflow==3.1.0 --no-deps
pip install mlflow-skinny==3.1.0 --no-deps
pip install flask sqlalchemy alembic scikit-learn pandas numpy joblib
```

## Utilisation

### 1. Lancer le serveur MLflow
```bash
python -m mlflow server --port 5000
```

### 2. Entraîner et tracker les modèles
```bash
python mlflow_tracking/mlflow_train.py
```

### 3. Ouvrir l'interface
Ouvrir dans le navigateur : **http://127.0.0.1:5000**

### 4. Monitoring
```bash
python monitoring/mlflow_monitoring.py
```

## Résultats

| Modèle | RMSE | MAE | R² |
|--------|------|-----|----|
| **Gradient Boosting** | **0.9483** | **0.7315** | **0.1826** |
| Random Forest | 0.9562 | 0.7367 | 0.1688 |
| Ridge Regression | 0.9822 | 0.7602 | 0.1229 |

**Modèle en production : Gradient Boosting (Version 6)**

## Charger le modèle (pour Amina — FastAPI)

```python
import mlflow.sklearn
mlflow.set_tracking_uri("http://127.0.0.1:5000")
model = mlflow.sklearn.load_model("models:/FilmRecommender@production")
```

## Expériences MLflow

| Expérience | Contenu |
|-----------|---------|
| `film-recommender` | Runs d'entraînement |
| `film-recommender-monitoring` | Runs de monitoring |