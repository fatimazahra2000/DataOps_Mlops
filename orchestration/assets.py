import subprocess
import sys
import os
import duckdb
from dagster import asset, MaterializeResult, MetadataValue

ROOT = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(ROOT, "movielens_pipeline.duckdb")
DBT_DIR = os.path.join(ROOT, "transform_data")


@asset
def ingestion_asset() -> MaterializeResult:
    result = subprocess.run(
        [sys.executable, "ingestion.py"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Échec ingestion : {result.stderr}")
    return MaterializeResult(metadata={"log": MetadataValue.text(result.stdout)})


@asset(deps=[ingestion_asset])
def dbt_transform_asset() -> MaterializeResult:
    result = subprocess.run(
        ["dbt", "run"], cwd=DBT_DIR, capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"Échec dbt run : {result.stdout}\n{result.stderr}")
    return MaterializeResult(metadata={"log": MetadataValue.text(result.stdout)})


@asset(deps=[dbt_transform_asset])
def dbt_test_asset() -> MaterializeResult:
    result = subprocess.run(
        ["dbt", "test"], cwd=DBT_DIR, capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"Échec dbt test : {result.stdout}\n{result.stderr}")
    return MaterializeResult(metadata={"log": MetadataValue.text(result.stdout)})


@asset(deps=[dbt_test_asset])
def data_quality_asset() -> MaterializeResult:
    con = duckdb.connect(DB_PATH)
    nulls = con.execute("""
        SELECT count(*) FROM recommandation_prete
        WHERE user_id IS NULL OR movie_id IS NULL OR rating IS NULL OR title IS NULL
    """).fetchone()[0]
    doublons = con.execute("""
        SELECT count(*) FROM (
            SELECT user_id, movie_id FROM recommandation_prete
            GROUP BY user_id, movie_id HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    hors_plage = con.execute("""
        SELECT count(*) FROM recommandation_prete
        WHERE rating < 0.5 OR rating > 5.0
    """).fetchone()[0]
    total_rows = con.execute("SELECT count(*) FROM recommandation_prete").fetchone()[0]
    con.close()

    if nulls > 0 or doublons > 0 or hors_plage > 0:
        raise Exception(f"Dataset invalide : {nulls} nulls, {doublons} doublons, {hors_plage} hors plage.")

    return MaterializeResult(metadata={
        "nombre_lignes": total_rows, "nulls": nulls,
        "doublons": doublons, "hors_plage": hors_plage,
    })


@asset(deps=[data_quality_asset])
def ml_ready_dataset_asset() -> MaterializeResult:
    notebooks = [
        "ML/prepare_data.ipynb",
        "ML/feature_engineering.ipynb",
        "ML/preprocessing.ipynb",
    ]
    for nb in notebooks:
        result = subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", nb],
            cwd=ROOT, capture_output=True, text=True, shell=True
        )
        if result.returncode != 0:
            raise Exception(f"Échec exécution {nb} : {result.stderr}")
    return MaterializeResult(metadata={"log": MetadataValue.text("Notebooks ML exécutés avec succès.")})