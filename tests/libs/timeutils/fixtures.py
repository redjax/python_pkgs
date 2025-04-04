from __future__ import annotations

from datetime import datetime

import pytest

__all__ = [
    "timestamp",
    "dt_str"
]

@pytest.fixture
def timestamp() -> datetime:
    return datetime.now()

@pytest.fixture
def dt_str() -> str:
    return "09:57:00"
