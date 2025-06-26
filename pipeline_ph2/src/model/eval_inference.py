import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error


def evaluate_and_predict(data_path: str, model_path: str, predictions_path: str) -> None:
    """Evaluate model performance and output predictions.

    Args:
        data_path: Path to the evaluation dataset.
        model_path: Path to the trained model file.
        predictions_path: Destination path for predictions parquet file.
    """
    df = pd.read_parquet(data_path)
    int_cols = df.select_dtypes(include=["int", "int64"]).columns.tolist()
    df = df[int_cols]
    y_true = df["SalePrice"]
    X = df.drop(columns=["SalePrice"])
    model = joblib.load(model_path)
    preds = model.predict(X)
    rmse = mean_squared_error(y_true, preds)
    print(f"RMSE on all data: {rmse}")
    pd.DataFrame({"Id": df["Id"], "prediction": preds}).to_parquet(
        predictions_path,
        index=False,
    )
