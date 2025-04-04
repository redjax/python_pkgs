from __future__ import annotations

import pytest

__all__ = ["temp_log_file"]

@pytest.fixture
def temp_log_file(tmp_path):
    return str(tmp_path / "test.log")
