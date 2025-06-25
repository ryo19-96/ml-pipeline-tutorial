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
    from model.eval_inference import evaluate_and_predict as _evaluate

    _evaluate(data.uri, model.path, predictions.uri)
