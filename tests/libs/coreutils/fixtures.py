import pytest

__all__ = [
    "sample_input_str",
    "sample_encoding",
    "sample_list",
    "empty_list",
    "single_item_list",
    "string_list",
    "normal_filename",
    "filename_with_spaces",
    "filename_with_unsafe_chars",
    "filename_with_mixed_issues",
    "filename_with_leading_trailing_issues",
    "empty_filename",
    "filename_with_only_unsafe_chars"
]

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

@pytest.fixture
def normal_filename():
    return "normal_file.txt"

@pytest.fixture
def filename_with_spaces():
    return "file with spaces.txt"

@pytest.fixture
def filename_with_unsafe_chars():
    return "file<with>unsafe:chars?.txt"

@pytest.fixture
def filename_with_mixed_issues():
    return "file with spaces and <unsafe> chars.txt"

@pytest.fixture
def filename_with_leading_trailing_issues():
    return "  ?file with issues?.txt  "

@pytest.fixture
def empty_filename():
    return ""

@pytest.fixture
def filename_with_only_unsafe_chars():
    return "<>:\"/\\|?*"