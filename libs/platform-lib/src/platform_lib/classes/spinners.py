from __future__ import annotations

from contextlib import AbstractContextManager
import itertools
import sys
import threading
import time

__all__ = ["CLISpinner"]


class CLISpinner(AbstractContextManager):
    """Show a CLI spinner in a new thread (disappears when context manager exits).

    Description:
        Wrap a function call in `with CLISpinner(message="..."):` to show a spinner in the CLI as the operation runs.
        When the operation completes, the spinner will disappear.

        Useful for providing feedback to user on longer running operations.
    """

    def __init__(self, message: str = "Processing..."):
        self.message = message
        self.stop_event = threading.Event()
        self.spinner_thread = threading.Thread(target=self._spin)

    def __enter__(self):
        self.spinner_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        self.spinner_thread.join()
        # Clear the line after the spinner stops
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()

    def _spin(self):
        spinner_cycle = itertools.cycle(["|", "/", "-", "\\"])
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r{self.message} {next(spinner_cycle)}")
            sys.stdout.flush()
            time.sleep(0.1)
