import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import time

DATA_DIR = "ML/processed"

print("Chargement des données...")
X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv")).values.ravel()
X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv")).values.ravel()

# Vérification des valeurs manquantes
print(f"Valeurs manquantes dans X_train : {X_train.isna().sum().sum()}")
print(f"Valeurs manquantes dans X_test  : {X_test.isna().sum().sum()}")

models = {
    "Ridge Regression": make_pipeline(SimpleImputer(strategy="median"), Ridge(alpha=1.0, random_state=42)),
    "Random Forest": make_pipeline(SimpleImputer(strategy="median"), RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)),
    "Gradient Boosting": make_pipeline(SimpleImputer(strategy="median"), GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)),
}

results = []

for name, model in models.items():
    print(f"\n--- Entraînement : {name} ---")
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    print(f"RMSE : {rmse:.4f}")
    print(f"MAE  : {mae:.4f}")
    print(f"Temps d'entraînement : {train_time:.2f}s")

    results.append({"Modèle": name, "RMSE": rmse, "MAE": mae, "Temps (s)": train_time})

print("\n=== Tableau comparatif ===")
df_results = pd.DataFrame(results).sort_values("RMSE")
print(df_results.to_string(index=False))