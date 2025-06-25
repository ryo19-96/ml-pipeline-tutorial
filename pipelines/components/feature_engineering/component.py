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
    from model.feature_extracton import create_features

    create_features(data.uri, output_data.uri)
