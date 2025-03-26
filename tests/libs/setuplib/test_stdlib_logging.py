import pytest
import logging
import logging
import logging.handlers
from pathlib import Path
import setup

from .fixtures import temp_log_file

def test_get_rotating_file_handler(temp_log_file):
    handler = setup.get_rotating_file_handler(temp_log_file)
    assert isinstance(handler, logging.handlers.RotatingFileHandler)
    assert handler.baseFilename == temp_log_file
    assert handler.maxBytes == 10 * 1024 * 1024
    assert handler.backupCount == 5

def test_get_timed_rotating_file_handler(temp_log_file):
    handler = setup.get_timed_rotating_file_handler(temp_log_file)
    assert isinstance(handler, logging.handlers.TimedRotatingFileHandler)
    assert handler.baseFilename == temp_log_file
    assert handler.when == 'midnight' or 'MIDNIGHT'
    assert handler.backupCount == 7

def test_setup_logging_basic(temp_log_file):
    setup.setup_logging(level="INFO", filename=temp_log_file)
    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO
    assert any(isinstance(h, logging.FileHandler) for h in root_logger.handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers)

def test_setup_logging_error_file(temp_log_file):
    error_file = temp_log_file + ".error"
    setup.setup_logging(level="INFO", filename=temp_log_file, error_filename=error_file)
    root_logger = logging.getLogger()
    assert any(isinstance(h, logging.FileHandler) and h.level == logging.ERROR for h in root_logger.handlers)

def test_setup_logging_invalid_level():
    with pytest.raises(ValueError):
        setup.setup_logging(level="INVALID_LEVEL")

def test_setup_logging_silence_loggers():
    test_logger = logging.getLogger("test_logger")
    setup.setup_logging(silence_loggers=["test_logger"])
    assert not test_logger.propagate

def test_setup_logging_rotating_handler(temp_log_file):
    setup.setup_logging(level="INFO", filename=temp_log_file, use_rotating_handler=True)
    root_logger = logging.getLogger()
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in root_logger.handlers)

@pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_setup_logging_levels(level, temp_log_file):
    setup.setup_logging(level=level, filename=temp_log_file)
    root_logger = logging.getLogger()
    assert root_logger.level == getattr(logging, level)

def test_setup_logging_custom_handlers(temp_log_file):
    custom_handler = logging.StreamHandler()
    setup.setup_logging(level="INFO", filename=temp_log_file, handlers=[custom_handler])
    root_logger = logging.getLogger()
    assert custom_handler in root_logger.handlers

@pytest.fixture(autouse=True)
def cleanup_logging():
    yield
    logging.getLogger().handlers.clear()
