# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "loguru",
#     "pandas",
#     "pandas-lib",
#     "pyarrow",
#     "sqlalchemy",
# ]
#
# [tool.uv.sources]
# pandas-lib = { path = "../../libs/pandas-lib" }
# ///
from __future__ import annotations

from loguru import logger as log
import pandas as pd
import pd_utils

if __name__ == "__main__":
    log.info("pd_utils sandbox")

    log.info("Creating a DataFrame")
    df: pd.DataFrame = pd.DataFrame({"A": [1, 3, 2], "B": [4, 5, 6]})

    log.info("Displaying DataFrame")
    log.info(f"Dataframe:\n{df.head(5)}")
    
    sorted_col_df = pd_utils.sort_df_by_col(df, "A")
    log.info(f"Dataframe sorted:\n{sorted_col_df.head(5)}")
