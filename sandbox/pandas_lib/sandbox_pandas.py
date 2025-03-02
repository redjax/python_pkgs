# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "loguru",
#     "pandas",
#     "pyarrow",
#     "sqlalchemy",
# ]
# ///

from loguru import logger as log
import pd_utils

import pandas as pd

if __name__ == "__main__":
    log.info("pd_utils sandbox")

    log.info("Creating a DataFrame")
    df: pd.DataFrame = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

    log.info("Displaying DataFrame")
    print(df.head(5))