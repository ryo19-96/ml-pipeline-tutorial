select
    *,
    (YrSold - YearBuilt) as AgeOfHouse,
    (YrSold - YearRemodAdd) as AgeSinceRemodel,
    (`1stFlrSF` + `2ndFlrSF` + TotalBsmtSF) as TotalSF,
    (YrSold - GarageYrBlt) as AgeOfGarage,
    (FullBath + HalfBath * 0.5 + BsmtFullBath + BsmtHalfBath * 0.5) as TotalBathrooms
from
    `pipeline-tutorial-463902.house_prices_dataset.train_data`
# 開発中はlimitしておく
limit
    100
