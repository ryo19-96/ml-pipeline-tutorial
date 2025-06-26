import gzip
import logging
import os
from patglib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    return df
