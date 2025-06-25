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
    from model.train import train_model

    train_model(data.uri, model.path)
