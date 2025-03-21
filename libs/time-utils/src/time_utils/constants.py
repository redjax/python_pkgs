"""Constant variables for `datetime` functions.

- TIME_FMT_24H (str): "%Y-%m-%d_%H:%M:%S"
- TIME_FMT_12H (str): "%Y-%m-%d_%I:%M:%S%p"
"""

from __future__ import annotations

__all__ = ["TIME_FMT_24H", "TIME_FMT_12H"]

TIME_FMT_24H: str = "%Y-%m-%d_%H:%M:%S"
TIME_FMT_12H: str = "%Y-%m-%d_%I:%M:%S%p"
