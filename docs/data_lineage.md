# Data Lineage

data/movies.csv, ratings.csv, tags.csv, links.csv
   → ingestion.py (dlt)
   → DuckDB : raw_data.movies, raw_data.ratings, raw_data.tags, raw_data.links
   → dbt (recommandation_prete.sql) : jointure raw_data.ratings + raw_data.movies
   → recommandation_prete (table finale, Data Contract enforced)
   → data_quality_check.py (validation qualité)
   → ML/prepare_data.ipynb (Yousera)