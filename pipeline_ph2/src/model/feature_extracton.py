import pandas as pd


def create_features(input_path: str, output_path: str) -> None:
    """Create additional features and save the result.

    Args:
        input_path: Path to the input parquet dataset.
        output_path: Destination path for the processed dataset.
    """
    df = pd.read_parquet(input_path)
    df["TotalPorchSF"] = df["OpenPorchSF"] + df["EnclosedPorch"] + df["3SsnPorch"] + df["ScreenPorch"]
    df = df.fillna(0)
    df.to_parquet(output_path, index=False)
