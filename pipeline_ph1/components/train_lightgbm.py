from kfp.v2.dsl import Dataset, Input, Model, Output, component


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
def train_lightgbm(
    train_path: Input[Dataset],
    target_path: Input[Dataset],
    model: Output[Model],
) -> None:
    """LightGBMモデルを学習するコンポーネント

    Args:
        train_path: 学習用データセットのパス
        target_path: 学習用目的変数のパス
        model: 学習済みモデルの保存先パス
    """

    import os
    from pathlib import Path

    import joblib
    import pandas as pd
    from lightgbm import LGBMRegressor

    def _save_model(model: LGBMRegressor, model_dir: str) -> None:
        """モデルを保存する

        Args:
            model: 学習済みモデル
            model_dir: モデルの保存先ディレクトリ
        """
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        joblib.dump(model, os.path.join(model_dir, "model.pkl"))

    def train_model(train_path: str, target_path: str, model_dir: str) -> None:
        """モデルを学習し保存するコンポーネント

        Args:
            data_path: 入力データセットのパス
            model_path: 学習済みモデルの保存先パス
        """
        train_df = pd.read_parquet(train_path)
        target_df = pd.read_parquet(target_path)

        model = LGBMRegressor(
            random_state=42,
            metric="rmse",
            max_depth=6,
            num_leaves=30,
        )
        model.fit(train_df, target_df)

        # モデルを保存
        _save_model(model, model_dir)

    # モデルの学習を実行
    train_path = f"{train_path.uri}.parquet"
    target_path = f"{target_path.uri}.parquet"
    train_model(train_path, target_path, model.path)
