from kfp.v2.dsl import Dataset, Output, component


@component(
    base_image="python:3.10",
    packages_to_install=["google-cloud-bigquery"],
)
def query_bigquery_to_gcs(
    query_str: str,
    bucket: str,
    path_prefix: str,
    output_path: Output[Dataset],
    project: str,
    location: str,
) -> None:
    """クエリを実行し、BigQuery テーブルから GCS にエクスポートするコンポーネント

    Args:
        sql_file (str): 実行する SQL クエリのファイルパス
        bucket (str): 出力先の GCS バケット名
        path_prefix (str): 出力ファイルのパスプレフィックス
        location (str): BigQuery のロケーション（デフォルトは 'asia-northeast1'）

    Returns:
        None

    Notes:
        クエリ結果を直接GCSに保存することはできないため、一時テーブルに保存してから保存する。
        永続テーブルに保存する場合は、destination テーブルを指定する必要がある。
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=project, location=location)

    # 一時テーブルへのクエリ実行
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query_str, location=location, job_config=job_config)
    query_job.result()

    temp_table = query_job.destination

    # テーブルを GCS にエクスポート
    destination_uri = f"gs://{bucket}/{path_prefix}.parquet"
    extract_job_config = bigquery.ExtractJobConfig(destination_format="PARQUET")
    extract_job = client.extract_table(
        temp_table,
        job_config=extract_job_config,
        destination_uris=destination_uri,
        location=location,
    )
    extract_job.result()

    # 出力パスを設定
    output_path.uri = destination_uri
