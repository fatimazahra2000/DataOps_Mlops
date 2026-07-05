import dlt
import pandas as pd
import os
DATA_DIR = os.environ.get("DATA_DIR", "data")

def run_ingestion():
    print("Lecture des fichiers CSV...")
    movies_df = pd.read_csv(f'{DATA_DIR}/movies.csv')
    ratings_df = pd.read_csv(f'{DATA_DIR}/ratings.csv')
    tags_df = pd.read_csv(f'{DATA_DIR}/tags.csv')
    links_df = pd.read_csv(f'{DATA_DIR}/links.csv')

    print(f"Données chargées : {len(movies_df)} films, {len(ratings_df)} notes, {len(links_df)} liens.")

    pipeline = dlt.pipeline(
        pipeline_name="movielens_pipeline",
        destination="duckdb",
        dataset_name="raw_data"
    )

    load_info = pipeline.run(
        [
            dlt.resource(movies_df, name="movies", write_disposition="replace"),
            dlt.resource(ratings_df, name="ratings", write_disposition="replace"),
            dlt.resource(tags_df, name="tags", write_disposition="replace"),
            dlt.resource(links_df, name="links", write_disposition="replace"),
        ]
    )

    print("--- Rapport d'ingestion ---")
    print(load_info)

if __name__ == "__main__":
    run_ingestion()