from kfp.v2.dsl import Dataset, Input, Output, component


@component(
    base_image="python:3.10",
    packages_to_install=[
        "pandas",
        "scikit-learn",
        "pyarrow",
        "gcsfs",
    ],
)
def split_data(
    data: Input[Dataset],
    train_features: Output[Dataset],
    train_target: Output[Dataset],
    valid_features: Output[Dataset],
    valid_target: Output[Dataset],
    test_features: Output[Dataset],
) -> None:
    """LightGBMモデルを学習するコンポーネント
    簡易的に1つのデータセットを学習用、検証用、推論用に分割する

    Args:
        data: 入力データセットのパス
    """

    import pandas as pd
    from sklearn.model_selection import train_test_split

    # データ分割
    df = pd.read_parquet(data.uri)
    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]

    # 学習用、検証用、推論用に分ける
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.5,
        random_state=123,
    )
    # 本来推論用の目的変数は知り得ないので不要
    X_valid, X_test, y_valid, _ = train_test_split(
        X_temp,
        y_temp,
        test_size=0.5,
        random_state=123,
    )

    X_train.to_parquet(f"{train_features.path}.parquet", index=False)
    X_valid.to_parquet(f"{valid_features.path}.parquet", index=False)
    X_test.to_parquet(f"{test_features.path}.parquet", index=False)
    y_train.to_frame().to_parquet(f"{train_target.path}.parquet", index=False)
    y_valid.to_frame().to_parquet(f"{valid_target.path}.parquet", index=False)
