import pytest

__all__ = ["sample_input_str", "sample_encoding"]

@pytest.fixture
def sample_input_str():
    return "This is a test string to be hashed."

@pytest.fixture
def sample_encoding():
    return "utf-8"
