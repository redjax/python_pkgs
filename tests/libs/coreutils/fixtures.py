import pytest

__all__ = ["sample_input_str", "sample_encoding", "sample_list", "empty_list", "single_item_list", "string_list"]

@pytest.fixture
def sample_input_str():
    return "This is a test string to be hashed."

@pytest.fixture
def sample_encoding():
    return "utf-8"

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def empty_list():
    return []

@pytest.fixture
def single_item_list():
    return [42]

@pytest.fixture
def string_list():
    return ["apple", "banana", "cherry", "date"]
