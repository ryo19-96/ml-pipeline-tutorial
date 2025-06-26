from kfp.v2.dsl import Dataset, Input, Output, component


@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "pyarrow", "gcsfs"],
)
def feature_engineering(
    data: Input[Dataset],
    output_data: Output[Dataset],
) -> None:
    """特徴量エンジニアリングを行うコンポーネント

    Args:
        data: 入力データセットのパス
        output_data: 出力データセットのパス
    """
    import pandas as pd

    def _save_df(df: pd.DataFrame, output_path: str) -> None:
        """データフレームをParquet形式で保存する

        Args:
            df: 保存するデータフレーム
            output_path: 出力データセットのパス
        """
        df.to_parquet(f"{output_path}/feature.parquet", index=False)

    def create_features(input_path: str, output_path: str) -> None:
        """特徴量エンジニアリングを行う

        Args:
            input_path: 入力データセットのパス
            output_path: 出力データセットのパス
        """
        df = pd.read_parquet(input_path)
        df["TotalPorchSF"] = df["OpenPorchSF"] + df["EnclosedPorch"] + df["3SsnPorch"] + df["ScreenPorch"]
        df = df.fillna(0)
        # 簡略化のため、数値型の列のみを抽出
        int_cols = df.select_dtypes(include=["number"]).columns.tolist()
        df = df[int_cols]

        _save_df(df, output_path)

    # 特徴量エンジニアリングを実行
    create_features(data.uri, output_data.uri)
