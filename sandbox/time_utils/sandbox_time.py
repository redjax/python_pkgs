# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "loguru",
#     "time-utils",
# ]
#
# [tool.uv.sources]
# time-utils = { path = "../../libs/time-utils" }
# ///
from __future__ import annotations

from loguru import logger as log
import time_utils

if __name__ == "__main__":
    log.info("Start time_utils sandbox")
    
    ts = time_utils.get_ts()
    log.info(f"Timestamp: {ts}")
    
    time_24h = time_utils.datetime_as_str(ts=ts, format=time_utils.TIME_FMT_24H)
    time_12h = time_utils.datetime_as_str(ts=ts, format=time_utils.TIME_FMT_12H)
    log.info(f"Timestamp: {time_24h} (24h), {time_12h} (12h)")
