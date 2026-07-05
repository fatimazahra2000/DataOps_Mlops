import duckdb
import os
DB_PATH = os.environ.get("DUCKDB_PATH", "movielens_pipeline.duckdb")

conn = duckdb.connect(DB_PATH)

print("Schémas :")
print(conn.execute("SHOW SCHEMAS").fetchall())

print("\nToutes les tables :")
print(conn.execute("SHOW ALL TABLES").fetchdf())

print("\nAperçu des films :")
print(conn.execute("SELECT * FROM raw_data.movies LIMIT 5").fetchdf())

conn.close()