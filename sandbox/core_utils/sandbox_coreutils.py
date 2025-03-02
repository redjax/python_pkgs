# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "coreutils-lib",
#     "loguru",
# ]
#
# [tool.uv.sources]
# coreutils-lib = { path = "../../libs/coreutils-lib" }
# pandas-lib = { path = "../../libs/pandas-lib" }
# ///

from loguru import logger as log

from core_utils import path_utils, hash_utils, list_utils, time_utils, uuid_utils

if __name__ == "__main__":
    log.info("core_utils sandbox")

    # log.info("Creating a DataFrame")
    # df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
