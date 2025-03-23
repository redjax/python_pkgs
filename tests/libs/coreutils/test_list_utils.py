# tests/libs/coreutils/test_list_utils.py
import pytest
from core_utils import list_utils

# Import fixtures
from .fixtures import sample_list, empty_list, single_item_list, string_list

__all__ = [
    "test_shuffle_list",
    "test_shuffle_empty_list",
    "test_shuffle_single_item_list",
    "test_get_random_item",
    "test_get_random_item_single_item",
    "test_get_random_item_empty_list",
    "test_get_random_index",
    "test_get_random_index_single_item",
    "test_get_random_index_empty_list",
    "test_functions_with_different_lists"
]

def test_shuffle_list(sample_list):
    shuffled = list_utils.shuffle_list(sample_list)
    assert len(shuffled) == len(sample_list)
    assert set(shuffled) == set(sample_list)
    assert shuffled != sample_list  # This might rarely fail due to randomness

def test_shuffle_empty_list(empty_list):
    assert list_utils.shuffle_list(empty_list) == []

def test_shuffle_single_item_list(single_item_list):
    assert list_utils.shuffle_list(single_item_list) == single_item_list

def test_get_random_item(sample_list):
    item = list_utils.get_random_item(sample_list)
    assert item in sample_list

def test_get_random_item_single_item(single_item_list):
    assert list_utils.get_random_item(single_item_list) == 42

def test_get_random_item_empty_list(empty_list):
    with pytest.raises(IndexError):
        list_utils.get_random_item(empty_list)

def test_get_random_index(sample_list):
    index = list_utils.get_random_index(sample_list)
    assert 0 <= index < len(sample_list)

def test_get_random_index_single_item(single_item_list):
    assert list_utils.get_random_index(single_item_list) == 0

def test_get_random_index_empty_list(empty_list):
    with pytest.raises(ValueError):
        list_utils.get_random_index(empty_list)

@pytest.mark.parametrize("test_list", [
    "sample_list",
    "string_list",
    "single_item_list"
])
def test_functions_with_different_lists(test_list, request):
    test_data = request.getfixturevalue(test_list)
    
    shuffled = list_utils.shuffle_list(test_data)
    assert len(shuffled) == len(test_data)
    assert set(shuffled) == set(test_data)

    item = list_utils.get_random_item(test_data)
    assert item in test_data

    index = list_utils.get_random_index(test_data)
    assert 0 <= index < len(test_data)