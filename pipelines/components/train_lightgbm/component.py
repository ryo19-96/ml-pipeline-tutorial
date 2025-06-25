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
    data: Input[Dataset],
    model: Output[Model],
) -> None:
    """Train a LightGBM model."""
    import joblib
    import pandas as pd
    from lightgbm import LGBMRegressor
    from sklearn.model_selection import train_test_split

    df = pd.read_parquet(data.uri)
    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )

    model_lgb = LGBMRegressor(random_state=42)
    model_lgb.fit(X_train, y_train)

    joblib.dump(model_lgb, model.path)
