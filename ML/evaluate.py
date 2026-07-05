import pandas as pd
import joblib
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

DATA_DIR = "ML/processed"
MODEL_PATH = "ML/models/model.pkl"

print("Chargement du modèle...")
model = joblib.load(MODEL_PATH)

print("Chargement des données de test...")
X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv"))
y_test = y_test.values.ravel()

print("Prédiction sur le jeu de test...")
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print("--- Résultats de l'évaluation ---")
print(f"RMSE : {rmse:.4f}")
print(f"MAE  : {mae:.4f}")