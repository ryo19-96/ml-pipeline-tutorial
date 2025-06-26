import joblib
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split


def train_model(data_path: str, model_path: str) -> None:
    """Train a LightGBM model and persist it.

    Args:
        data_path: Path to the input parquet dataset.
        model_path: Destination path for the serialized model.
    """
    df = pd.read_parquet(data_path)
    int_cols = df.select_dtypes(include=["int", "int64"]).columns.tolist()
    df = df[int_cols]
    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]

    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = LGBMRegressor(random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
