import pytest
from datetime import datetime

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
