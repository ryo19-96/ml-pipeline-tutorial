# ml-pipeline-tutorial


## 概要

本リポジトリは、研修生がクラウドサービスや機械学習パイプラインの基礎を学ぶことを目的としたチュートリアルプロジェクトです。  
Google Cloud の Vertex AI Pipelines（KFP v2 SDK）を活用し、データの前処理からモデルの学習・評価・保存までの一連の処理を自動化する簡易的な ML パイプラインを構築しています。クラウド上での開発・運用体験を通じて、MLOps の基礎的な理解と GCP リソースの取り扱いに慣れることを目的としています。
なお Vertex AI では TFX と KFPv2 の 2 通りのパイプラインの作成方法がサポートされていますが、今回は KFPv2 SDK を用いて作成します。  
※KFP (Kubeflow Pipelines) バージョン1.8は2024年12月にサポートが終了し、バージョン2.0へ移行しました。pipelineの書き方が大きく変わっているため調べる際は注意してください。


## 使用データ

以下のデータを利用しています
 - 出典：kaggle House Prices - Advanced Regression Techniques
 - URL：https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data
 - 内容：住宅の特徴量（床面積、築年数、立地等）を元に住宅価格を予測する回帰タスク

## セットアップ手順（開発環境の構築）
**※ 現時点では研修生の GCP 権限やプロジェクト登録方針が未定です。Terraform の管理方針については別途ご相談ください**  
**terraformの管理をどうするかも別途相談させてください**
  
仮想環境下での実施を推奨

1. gcloudのインストール (参照：[gcloud CLI をインストールする](https://cloud.google.com/sdk/docs/install?hl=ja))
2. google cloudで任意のプロジェクトを作成
   - プロジェクトが複数ある場合はローカルの設定を切り替える必要あり (参照：[gcloud でプロジェクトの切り替え設定](https://qiita.com/sonots/items/906798c408132e26b41c))
3. uv & 仮想環境のセットアップ
    ```sh
    # uv のインストール（グローバル）
    python3 -m pip install --upgrade uv
    
    # プロジェクトルート
    uv venv .venv
    source .venv/bin/activate
    uv sync
    ```
4. terraformのインストール (参照：[Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli))
5. `/terraform/variables.tf`を作成したプロジェクトにあわせます。以下を修正してください
    #### 変数の意味

    - `project_id`  
    GCP プロジェクト ID。手順 2 で作成したものに置き換えてください。

    - `region` / `zone`  
    リソースを配置するリージョンとゾーン。

    - `pipeline_bucket_name`  
    Vertex AI Pipeline が中間データを出力するバケット名。GCS のバケット名はグローバル一意なので、他とかぶらない名称にしてください。

    - `house_prices_data_bucket_name`  
    Kaggle から取得した生データを格納する専用バケット。

    - `docker_repo_id`  
    Artifact Registry のリポジトリ名。`docker push` 先になります。
6. terraformを実行します
    ```sh 
    make terraform_init
    make terraform_apply
    ```
7. google cloud上で以下を確認してください
   - GCSにバケットが作成されている
   - Artifact Registry のリポジトリが作成されている
8. kaggleのtrain.csvをローカルに保存し、以下のコマンドでGCSへ保存→BQへ保存します
    ```sh
    # データをGCSに保存
    gsutil cp ~/downloads/train_house.csv gs://{data_bucket}/train.csv

    # GCSのデータを作成したテーブルへアップロード
    bq load \       
    --source_format=CSV \
    --autodetect \
    house_prices_dataset.train_data \                         
    gs://{data_bucket}/train.csv
    ```
9. `pipeline_ph1/pipelines/house_prices_pipeline.py`で以下を修正してください
    ```python
    PROJECT_ID = "{your_project_id}"
    LOCATION = "{your_location}"
    PIPELINE_BUCKET = "{your_pipeline_bucket_name}"
    ```
10. 以下コマンドで`pipeline_ph1/pipelines/house_prices_pipeline.py`が実行されます。  

    ```sh
    make pipeline_run
    # キャッシュを利用したい場合は以下コマンド
    make pipeline_run enable_cache=True              
    ```
11. ターミナルに表示される View Pipeline Job のリンクから飛ぶか、コンソール上からvertex ai pipeline へ行きpipelineが実行されていることを確認してください。



## 今後の拡張アイデア（研修課題例）

- 特徴量エンジニアリングの工夫
  - クエリでの計算追加、カテゴリ特徴量の追加、ログ変換、欠損値の処理変更など

- パイプライン構成の改良
  - 評価と推論のコンポーネントを分離する

- 設定の外部化
  - 学習パラメータを YAML ファイルで管理し、柔軟に変更可能にする

- 推論時のデータをkaggleのtest.csvを使用する形にする

などなど