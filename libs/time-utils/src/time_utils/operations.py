from __future__ import annotations

import logging

log = logging.getLogger()

import datetime as dt
import time
from typing import Union

from .constants import TIME_FMT_12H, TIME_FMT_24H

__all__ = [
    "datetime_as_dt",
    "datetime_as_str",
    "get_ts",
    "wait",
]


def datetime_as_str(ts: dt = None, format: str = TIME_FMT_24H) -> str:
    """Convert a `datetime.datetime` object to a string.

    Params:
        ts (datetime.datetime): A Python `datetime.datetime` object to convert to a `str`
        format (str): The `str` time string format to use

    Returns:
        (str): A formatted `datetime.datetime` `str`

    """
    _ts: str = ts.strftime(format=format)

    return _ts


def datetime_as_dt(ts: str = None, format: str = TIME_FMT_24H) -> dt:
    """Convert a datetime string to a `datetime.datetime` object.

    Params:
        ts (str): A datetime str to convert to a Python `datetime.datetime` object
        format (str): The `str` time string format to use

    Returns:
        (str): A formatted `datetime.datetime` object

    """
    _ts: dt = dt.strptime(ts, format)

    return _ts


def get_ts(as_str: bool = False, format: str = TIME_FMT_24H) -> Union[dt.datetime, str]:
    """Get a timestamp object.

    Params:
        as_str (bool): If `True`, converts `datetime` to a `str`
        format (str): The `str` time string format to use

    Returns:
        (datetime.datetime): a Python `datetime.datetime` object.
        (str): If `as_str` is `True`, converts datetime to a string & returns.

    """
    now: dt = dt.now()

    if as_str:
        now: str = datetime_as_str(ts=now, format=format)

    return now


def get_next_full_hour(now: dt.datetime | None = None) -> dt.datetime:
    """Return the next full hour datetime after `now`. If `now` is None, uses current time.

    Examples:
        1:30  -> 2:00
        8:16  -> 9:00
        23:59 -> next day 00:00

    """
    if now is None:
        now = dt.datetime.now()

    ## Replace minutes, seconds, microseconds with zero
    next_hour = now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)

    return next_hour


def wait(s: int = 1, msg: str | None = "Waiting {} seconds...") -> None:
    """Sleep for a number of seconds, with optional custom message.

    Params:
        s (int): Amount of time (in seconds) to sleep/pause.
        msg (str): [default: 'Wating {} seconds...'] A custom message to print. Use {} in the
            message to print the value of s.

                Example: 'I will now wait for {} second(s)' => 'I will now wait for 15 seconds...'
    """
    assert s, ValueError("Missing amount of time to sleep")
    assert isinstance(s, int) and s > 0, ValueError(
        f"Value of s must be a positive, non-zero integer. Input value ({type(s)}): {s} is invalid."
    )

    ## If msg != None, validate & print before pausing
    if msg:
        try:
            ## Validate & print pause message
            assert isinstance(msg, str), TypeError(
                f"msg must be a string or None. Got type: ({type(msg)})"
            )

            try:
                log.info(msg.format(s))
            except Exception as exc:
                ## Error compiling message text. Print an error, then wait
                msg = Exception(
                    f"Unhandled exception composing wait message. Details: {exc}.\nWaiting [{s}] seconds..."
                )
                log.error(msg)

        except Exception as exc:
            ## Error compiling message text. Print an error, then wait
            msg = Exception(
                f"Unhandled exception composing wait message. Details: {exc}\nWaiting [{s}] seconds..."
            )
            log.error(msg)

    ## Pause
    time.sleep(s)


if __name__ == "__main__":
    ts = get_ts()

    log.info(f"Timestamp ({type(ts)}): {ts}")

    as_str: str = get_ts(as_str=True)
    log.info(f"Timestamp: datetime to str Type({type(as_str).__name__}): {as_str}")

    as_dt: dt = datetime_as_dt(ts=as_str)
    log.info(f"Timestamp: str to datetime Type({type(as_dt).__name__}): {as_dt}")
