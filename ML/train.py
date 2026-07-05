import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import joblib
import os

DATA_DIR = "ML/processed"
MODEL_DIR = "ML/models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

print("Chargement des données d'entraînement...")
X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv"))
y_train = y_train.values.ravel()

print(f"Shape X_train : {X_train.shape}")
print(f"Shape y_train : {y_train.shape}")

print("Entraînement du modèle (GradientBoostingRegressor)...")
model = make_pipeline(
    SimpleImputer(strategy="median"),
    GradientBoostingRegressor(
        n_estimators=100,
        max_depth=3,
        random_state=42
    )
)
model.fit(X_train, y_train)
print("Entraînement terminé.")

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"Modèle sauvegardé dans : {MODEL_PATH}")