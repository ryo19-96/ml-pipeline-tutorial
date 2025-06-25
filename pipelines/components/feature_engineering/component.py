from kfp.v2.dsl import Dataset, Input, Output, component


@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "pyarrow", "gcsfs"],
)
def additional_feature_engineering(
    data: Input[Dataset],
    output_data: Output[Dataset],
) -> None:
    """Create additional features using pandas."""
    import pandas as pd

    df = pd.read_parquet(data.uri)
    df["TotalPorchSF"] = (
        df["OpenPorchSF"]
        + df["EnclosedPorch"]
        + df["3SsnPorch"]
        + df["ScreenPorch"]
    )
    df = df.fillna(0)
    df.to_parquet(output_data.uri, index=False)
