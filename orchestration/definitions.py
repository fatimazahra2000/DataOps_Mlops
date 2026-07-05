from dagster import Definitions, define_asset_job

from orchestration.assets import (
    ingestion_asset,
    dbt_transform_asset,
    dbt_test_asset,
    data_quality_asset,
    ml_ready_dataset_asset,
)

pipeline_complet_job = define_asset_job(
    name="pipeline_dataops_complet",
    selection="*",
)

defs = Definitions(
    assets=[
        ingestion_asset,
        dbt_transform_asset,
        dbt_test_asset,
        data_quality_asset,
        ml_ready_dataset_asset,
    ],
    jobs=[pipeline_complet_job],
)