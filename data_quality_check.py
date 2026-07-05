import duckdb
import sys
import os
DB_PATH = os.environ.get("DUCKDB_PATH", "movielens_pipeline.duckdb")

con = duckdb.connect(DB_PATH)

erreurs = []

nulls = con.execute("""
    SELECT count(*) FROM recommandation_prete
    WHERE user_id IS NULL OR movie_id IS NULL OR rating IS NULL OR title IS NULL
""").fetchone()[0]
if nulls > 0:
    erreurs.append(f"{nulls} lignes avec valeurs manquantes.")

doublons = con.execute("""
    SELECT count(*) FROM (
        SELECT user_id, movie_id FROM recommandation_prete
        GROUP BY user_id, movie_id HAVING COUNT(*) > 1
    )
""").fetchone()[0]
if doublons > 0:
    erreurs.append(f"{doublons} doublons (user_id, movie_id).")

hors_plage = con.execute("""
    SELECT count(*) FROM recommandation_prete
    WHERE rating < 0.5 OR rating > 5.0
""").fetchone()[0]
if hors_plage > 0:
    erreurs.append(f"{hors_plage} notes hors de la plage [0.5, 5.0].")

con.close()

if erreurs:
    print("❌ DATASET INVALIDE :")
    for e in erreurs:
        print(" -", e)
    sys.exit(1)
else:
    print("✅ Dataset validé : aucune anomalie détectée.")
    sys.exit(0)