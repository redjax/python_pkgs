from __future__ import annotations

from .fixtures import (
    empty_filename,
    filename_with_leading_trailing_issues,
    filename_with_mixed_issues,
    filename_with_only_unsafe_chars,
    filename_with_spaces,
    filename_with_unsafe_chars,
    normal_filename,
)

from core_utils import path_utils
import pytest

__all__ = [
    "test_sanitize_normal_filename",
    "test_sanitize_filename_with_spaces",
    "test_sanitize_filename_with_unsafe_chars",
    "test_sanitize_filename_with_mixed_issues",
    "test_sanitize_filename_with_leading_trailing_issues",
    "test_sanitize_empty_filename",
    "test_sanitize_filename_with_only_unsafe_chars",
    "test_sanitize_filename_custom_space_replacement",
    "test_sanitize_filename_custom_unsafe_char_replacement",
    "test_sanitize_filename_no_replacements"
]

def test_sanitize_normal_filename(normal_filename):
    assert path_utils.sanitize_filename(normal_filename) == normal_filename

def test_sanitize_filename_with_spaces(filename_with_spaces):
    sanitized = path_utils.sanitize_filename(filename_with_spaces)
    assert sanitized == "file_with_spaces.txt"
    assert " " not in sanitized

def test_sanitize_filename_with_unsafe_chars(filename_with_unsafe_chars):
    sanitized = path_utils.sanitize_filename(filename_with_unsafe_chars)
    assert sanitized == "file-with-unsafe-chars-.txt"
    assert all(char not in sanitized for char in "<>:\"/\\|?*")

def test_sanitize_filename_with_mixed_issues(filename_with_mixed_issues):
    sanitized = path_utils.sanitize_filename(filename_with_mixed_issues)
    assert sanitized == "file_with_spaces_and_-unsafe-_chars.txt"
    assert " " not in sanitized
    assert all(char not in sanitized for char in "<>:\"/\\|?*")

def test_sanitize_filename_with_leading_trailing_issues(filename_with_leading_trailing_issues):
    sanitized = path_utils.sanitize_filename(filename_with_leading_trailing_issues)
    assert sanitized == "file_with_issues-.txt"
    assert not sanitized.startswith((" ", "?", "-"))
    assert not sanitized.endswith((" ", "?", "-"))

def test_sanitize_empty_filename(empty_filename):
    assert path_utils.sanitize_filename(empty_filename) == ""

def test_sanitize_filename_with_only_unsafe_chars(filename_with_only_unsafe_chars):
    sanitized = path_utils.sanitize_filename(filename_with_only_unsafe_chars)
    ## All chars are replaced and then stripped
    assert sanitized == ""

@pytest.mark.parametrize("space_replacement", ["_", "-", ""])
def test_sanitize_filename_custom_space_replacement(filename_with_spaces, space_replacement):
    sanitized = path_utils.sanitize_filename(filename_with_spaces, space_replacement=space_replacement)
    assert sanitized == f"file{space_replacement}with{space_replacement}spaces.txt"

@pytest.mark.parametrize("unsafe_char_replacement", ["_", "X", ""])
def test_sanitize_filename_custom_unsafe_char_replacement(filename_with_unsafe_chars, unsafe_char_replacement):
    sanitized = path_utils.sanitize_filename(filename_with_unsafe_chars, unsafe_char_replacement=unsafe_char_replacement)
    expected = f"file{unsafe_char_replacement}with{unsafe_char_replacement}unsafe{unsafe_char_replacement}chars{unsafe_char_replacement}.txt"
    assert sanitized == expected.strip(unsafe_char_replacement)

def test_sanitize_filename_no_replacements():
    filename = "file<with>unsafe:chars?.txt"
    sanitized = path_utils.sanitize_filename(filename, space_replacement="", unsafe_char_replacement="")
    assert sanitized == "filewithunsafechars.txt"
