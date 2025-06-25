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
def evaluate_and_predict(
    data: Input[Dataset],
    model: Input[Model],
    predictions: Output[Dataset],
) -> None:
    """Evaluate the model and output predictions."""
    import joblib
    import pandas as pd
    from sklearn.metrics import mean_squared_error

    df = pd.read_parquet(data.uri)
    y_true = df["SalePrice"]
    X = df.drop(columns=["SalePrice"])
    mdl = joblib.load(model.path)
    preds = mdl.predict(X)
    rmse = mean_squared_error(y_true, preds, squared=False)
    print(f"RMSE on all data: {rmse}")

    pd.DataFrame({"Id": df["Id"], "prediction": preds}).to_parquet(
        predictions.uri, index=False,
    )
