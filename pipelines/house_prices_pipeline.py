from pathlib import Path

from components.query_bigquery.component import query_bigquery_to_gcs
from kfp import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import Dataset, Input, component


@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "pyarrow", "gcsfs"],
)
def read_csv_and_print_shape(data: Input[Dataset]) -> None:
    import pandas as pd

    df = pd.read_parquet(data.uri)
    print(f"Data shape: {df.shape}")


# pipeline definition
@dsl.pipeline(name="house-prices-pipeline")
def pipeline() -> None:
    query_str = (Path(__file__).parent / "sql" / "train_table.sql").read_text()
    bq_task = query_bigquery_to_gcs(
        location="asia-northeast1",
        project="pipeline-tutorial-463902",
        query_str=query_str,
        bucket="pipeline_tutorial_house_prices",
        path_prefix="house_prices/feature_engineering",
    )
    _ = read_csv_and_print_shape(data=bq_task.outputs["output_path"])


if __name__ == "__main__":
    FILE_NAME = Path(__file__).with_suffix(".json").name
    compiler.Compiler().compile(pipeline, FILE_NAME)

    from google.cloud import aiplatform
    from google.cloud.aiplatform import pipeline_jobs

    aiplatform.init(project="pipeline-tutorial-463902", location="asia-northeast1")
    job = pipeline_jobs.PipelineJob(
        display_name="house-prices-pipeline",
        pipeline_root="gs://pipeline_tutorial_house_prices",
        template_path=FILE_NAME,
    )
    job.submit(service_account="vertex-pipeline-sa@pipeline-tutorial-463902.iam.gserviceaccount.com")

    Path(FILE_NAME).unlink()
