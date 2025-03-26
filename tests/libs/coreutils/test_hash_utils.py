from __future__ import annotations

from .fixtures import sample_encoding, sample_input_str

from core_utils import hash_utils
import pytest

__all__ = ["test_hash_str", "test_hash_str_different_inputs", "test_hash_str_invalid_input", "test_hash_str_invalid_encoding"]


def test_hash_str(sample_input_str, sample_encoding):
    result = hash_utils.get_hash_from_str(input_str=sample_input_str, encoding=sample_encoding)
    
    assert isinstance(result, str)
    assert len(result) == 32

@pytest.mark.parametrize("input_str, expected_length", [
    ("", 32),
    ("a", 32),
    ("hello world", 32),
    ("1234567890", 32),
])
def test_hash_str_different_inputs(input_str, expected_length, sample_encoding):
    result = hash_utils.get_hash_from_str(input_str=input_str, encoding=sample_encoding)
    assert len(result) == expected_length

@pytest.mark.xfail(reason="Invalid input entered, test fail expected")
@pytest.mark.parametrize("invalid_input", [None, 123, [], {}])
def test_hash_str_invalid_input(invalid_input):
    with pytest.raises(ValueError):
        hash_utils.get_hash_from_str(input_str=invalid_input)

@pytest.mark.xfail(raises=LookupError, reason="Invalid encoding should fail", strict=True)
def test_hash_str_invalid_encoding(sample_input_str):
    ## Remove context manager since xfail handles expected exceptions
    hash_utils.get_hash_from_str(
        input_str=sample_input_str, 
        encoding="invalid_encoding"
    )
