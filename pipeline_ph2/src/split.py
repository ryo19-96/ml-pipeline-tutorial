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
