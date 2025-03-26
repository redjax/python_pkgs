import pytest
from datetime import datetime, timedelta
import re
import logging

from core_utils.time_utils import (
    datetime_as_str,
    datetime_as_dt,
    get_ts,
    wait
)
from core_utils.time_utils.constants import TIME_FMT_12H, TIME_FMT_24H

from .fixtures import timestamp, dt_str

def test_datetime_as_str(timestamp: datetime):
    # Test with default format (24-hour)
    result = datetime_as_str(timestamp)
    print(f"Default format result: {result}")
    assert re.match(r'^\d{4}-\d{2}-\d{2}[_ ]\d{2}:\d{2}:\d{2}$', result)

    # Test with 12-hour format
    result_12h = datetime_as_str(timestamp, format=TIME_FMT_12H)
    print(f"12-hour format result: {result_12h}")
    assert re.match(r'^\d{4}-\d{2}-\d{2}[_ ]\d{2}:\d{2}:\d{2}(AM|PM)$', result_12h)

    # Test with safe_str=True
    result_safe = datetime_as_str(timestamp, format="%Y-%m-%d %H:%M:%S", safe_str=True)
    print(f"Safe string result: {result_safe}")
    assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}$', result_safe)


def test_datetime_as_dt():
    # Match the format used in datetime_as_str's default
    test_str = "2025-03-26_09:57:00"  # Example matching "%Y-%m-%d_%H:%M:%S"
    result = datetime_as_dt(test_str)  # Default format now matches
    
    assert isinstance(result, datetime)
    assert result.year == 2025
    assert result.month == 3
    assert result.day == 26
    assert result.hour == 9
    assert result.minute == 57


def test_get_ts():
    # Test without parameters (returns datetime object)
    result = get_ts()
    assert isinstance(result, datetime)
    
    # Test with as_str=True (returns a formatted string)
    result_str = get_ts(as_str=True)
    assert isinstance(result_str, str)
    assert re.match(r'^\d{2}:\d{2}:\d{2}$', result_str)  # Validate 24-hour time format
    
    # Test with safe_str=True (returns a path-safe string)
    result_safe_str = get_ts(as_str=True, safe_str=True, format="%Y-%m-%d %H:%M:%S")
    assert isinstance(result_safe_str, str)
    assert ":" not in result_safe_str  # Ensure colons are replaced


def test_wait(caplog):
    start_time = datetime.now()
    
    # Call wait() and capture logs
    wait(1, msg="Custom wait message: {} seconds")
    
    end_time = datetime.now()
    
    # Verify that at least 1 second has passed
    elapsed_time = (end_time - start_time).total_seconds()
    assert elapsed_time >= 1
    
    # Check that the custom message was logged
    assert "Custom wait message: 1 seconds" in caplog.text


def test_wait_invalid_input():
    with pytest.raises(ValueError):
        wait(0)
    
    with pytest.raises(ValueError):
        wait(-1)
    
    with pytest.raises(ValueError):
        wait("invalid")


def test_wait_invalid_msg():
    # Should now raise ValueError instead of TypeError
    with pytest.raises(ValueError):
        wait(1, msg=123)


# Test get_ts function
def test_get_ts():
    # Test without parameters
    result = get_ts()
    assert isinstance(result, datetime)
    
    # Test with as_str=True
    result_str = get_ts(as_str=True)
    assert isinstance(result_str, str)
    
    # Test with safe_str=True
    result_safe_str = get_ts(as_str=True, safe_str=True)
    assert ":" not in result_safe_str

def test_wait(caplog):
    with caplog.at_level(logging.INFO):
        start_time = datetime.now()
        wait(1, msg="Custom wait message: 1 second")
        end_time = datetime.now()
    
    assert end_time - start_time >= timedelta(seconds=1)
    assert "Custom wait message: 1 second" in caplog.text

    # Debug: Print captured logs
    print("Captured logs:", caplog.text)

@pytest.mark.xfail
def test_wait_invalid_input():
    with pytest.raises(ValueError):
        wait(0)
    
    with pytest.raises(ValueError):
        wait(-1)
    
    with pytest.raises(ValueError):
        wait("invalid")

@pytest.mark.xfail
def test_wait_invalid_msg():
    with pytest.raises(TypeError):
        wait(1, msg=123)
