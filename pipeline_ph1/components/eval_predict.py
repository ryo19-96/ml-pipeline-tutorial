from kfp.v2.dsl import Dataset, Input, Metrics, Model, Output, component


@component(
    base_image="python:3.10",
    packages_to_install=[
        "pandas",
        "scikit-learn",
        "lightgbm",
        "joblib",
        "pyarrow",
        "gcsfs",
    ],
)
def evaluate_and_predict(
    model: Input[Model],
    valid_feature: Input[Dataset],
    valid_target: Input[Dataset],
    test_feature: Input[Dataset],
    outputs: Output[Dataset],
    metrics: Output[Metrics],
) -> None:
    """モデルの評価と予測を行うコンポーネント

    Args:
        data: 入力データセットのパス
        model: 学習済みモデルのパス
        predictions: 予測結果を保存する出力データセットのパス
    """

    import logging
    import os
    from pathlib import Path

    import joblib
    import pandas as pd
    from lightgbm import LGBMRegressor
    from sklearn.metrics import mean_squared_error

    logger = logging.getLogger(__name__)

    def _save(preds: pd.Series, output_path: str) -> None:
        """予測結果を保存する

        Args:
            preds: 予測結果のSeries
            output_path: 出力データセットのパス
        """
        Path(output_path).mkdir(parents=True, exist_ok=True)
        preds.to_frame(name="SalePrice").to_csv(f"{output_path}/predictions.csv", index=False)

    def _evaluation(
        valid_feature_path: str,
        valid_target_path: str,
        model: LGBMRegressor,
    ) -> float:
        """モデルの評価を行い、RMSEを返す

        Args:
            valid_feature_path: 検証用特徴量データセットのパス
            valid_target_path: 検証用ターゲットデータセットのパス
            model: 学習済みモデル

        Returns:
            RMSE値
        """
        X_valid = pd.read_parquet(valid_feature_path)
        y_true = pd.read_parquet(valid_target_path)

        preds = model.predict(X_valid)

        rmse = mean_squared_error(y_true, preds)
        logger.info(f"RMSE on validation data: {rmse}")
        return rmse

    def _prediction(
        test_feature_path: str,
        model: LGBMRegressor,
    ) -> pd.Series:
        """テストデータに対する予測を行う

        Args:
            test_feature_path: テスト用特徴量データセットのパス
            model: 学習済みモデル

        Returns:
            予測結果のSeries
        """
        X_test = pd.read_parquet(test_feature_path)
        preds = model.predict(X_test)
        return pd.Series(preds, name="SalePrice")

    def evaluate_and_predict(
        valid_feature_path: str,
        valid_target_path: str,
        test_feature_path: str,
        model_path: str,
    ) -> None:
        """モデルの評価と予測を行い、結果を保存

        Args:
            data_path: 入力データセットのパス
            model_path: 学習済みモデルのパス
            predictions_path: 予測結果を保存する出力データセットのパス
        """
        # モデルの読み込み
        model = joblib.load(model_path)

        # 検証データでの評価
        rmse = _evaluation(valid_feature_path, valid_target_path, model)
        metrics.log_metric("rmse", rmse)

        # テストデータでの予測
        preds = _prediction(test_feature_path, model)

        # 予測結果を保存
        _save(preds, outputs.path)

    # モデルの評価と予測を実行
    valid_feature_path = f"{valid_feature.uri}.parquet"
    valid_target_path = f"{valid_target.uri}.parquet"
    test_feature_path = f"{test_feature.uri}.parquet"
    model_path = os.path.join(model.path, "model.pkl")
    evaluate_and_predict(valid_feature_path, valid_target_path, test_feature_path, model_path)
