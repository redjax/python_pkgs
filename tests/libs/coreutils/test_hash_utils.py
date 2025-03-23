from core_utils import hash_utils


def test_hash_str(sample_input_str: str, sample_encoding: str = "utf-8"):
    result = hash_utils.get_hash_from_str(input_str=sample_input_str, encoding=sample_encoding)
    
    assert isinstance(result, str)
    assert len(result) == 32
