import argparse
from pathlib import Path

from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs
from kfp import dsl
from kfp.v2 import compiler

from pipeline_ph1.components.eval_predict import evaluate_and_predict
from pipeline_ph1.components.feature_engineering import feature_engineering
from pipeline_ph1.components.query_bigquery import query_bigquery_to_gcs
from pipeline_ph1.components.split import split_data
from pipeline_ph1.components.train_lightgbm import train_lightgbm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enable_cache", type=lambda x: x.lower() in ("true", "1"), default=False)
    return parser.parse_args()


# pipeline definition
@dsl.pipeline(name="house-prices-pipeline")
def house_prices_pipeline() -> None:
    # クエリを文字列として読み込む
    query_str = (Path(__file__).parent / "sql" / "train_table.sql").read_text()

    bq_op = (
        query_bigquery_to_gcs(
            location="asia-northeast1",
            project="pipeline-tutorial-463902",
            query_str=query_str,
            bucket="pipeline_tutorial_house_prices",
            path_prefix="house_prices/feature_engineering",
        )
        .set_display_name("query_bigquery_to_gcs")
        .set_caching_options(True)
        .set_cpu_limit("4")
        .set_memory_limit("16G")
    )

    feature_engineering_op = (
        feature_engineering(
            data=bq_op.outputs["output_path"],
        )
        .set_display_name("feature_engineering")
        .set_caching_options(True)
        .set_cpu_limit("4")
        .set_memory_limit("16G")
    )

    split_data_op = (
        split_data(data=feature_engineering_op.outputs["output_data"])
        .set_display_name("split_data")
        .set_caching_options(True)
        .set_cpu_limit("4")
        .set_memory_limit("16G")
    )

    model_op = (
        train_lightgbm(
            train_path=split_data_op.outputs["train_features"],
            target_path=split_data_op.outputs["train_target"],
        )
        .set_display_name("train_lightgbm")
        .set_caching_options(True)
        .set_cpu_limit("4")
        .set_memory_limit("16G")
    )

    _ = (
        evaluate_and_predict(
            valid_feature=split_data_op.outputs["valid_features"],
            valid_target=split_data_op.outputs["valid_target"],
            test_feature=split_data_op.outputs["test_features"],
            model=model_op.outputs["model"],
        )
        .set_display_name("evaluate_and_predict")
        .set_caching_options(True)
        .set_cpu_limit("4")
        .set_memory_limit("16G")
    )


if __name__ == "__main__":
    args = parse_args()
    # パイプラインをコンパイルして JSON ファイルに保存
    file_name = Path(__file__).with_suffix(".json").name
    compiler.Compiler().compile(house_prices_pipeline, file_name)

    # Google Cloud AI Platform にパイプラインを送信、実行
    aiplatform.init(project="pipeline-tutorial-463902", location="asia-northeast1")
    job = pipeline_jobs.PipelineJob(
        display_name="house-prices-pipeline",
        pipeline_root="gs://pipeline_tutorial_house_prices",
        template_path=file_name,
        enable_caching=args.enable_cache,
    )
    job.submit(service_account="vertex-pipeline-sa@pipeline-tutorial-463902.iam.gserviceaccount.com")

    # JSON ファイルを削除
    Path(file_name).unlink()
