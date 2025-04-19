import logging
import argparse
import typing as t
from decimal import Decimal
import multiprocessing
import platform as _platform
from types import ModuleType
import sys

from platform_lib.classes.converted_bytes import ConvertedBytes
from platform_lib.constants import VALID_FILESIZE_UNITS
from platform_lib.enums._enums import EnumMac, EnumUnix

log = logging.getLogger(__name__)

__all__ = [
    "_set_logging_level",
    "parse_args",
    "convert_bytes",
    "get_cpu_count",
    "get_platform_terse",
    "get_platform_aliased",
    "get_python_path",
    "get_python_modules",
    "get_sys_byteorder",
    "get_os_release",
    "get_libc_version",
    "get_freedesktop_release",
]


def _set_logging_level(
    verbosity: int,
    set_debug: bool = False,
    log_fmt: str = "%(module)s |> %(message)s",
    log_fmt_debug: str = (
        "%(levelname)s | [%(asctime)s] | [logger:%(name)s] | [%(funcName)s:%(lineno)s] |> %(message)s"
    ),
) -> None:
    """Handler function to configure logging & set verbosity/debugging from CLI options."""
    ## Cap verbosity at 2
    verbosity = min(verbosity, 2)

    if verbosity > 1:
        print("Setting log level to DEBUG")
        log_level: int = logging.DEBUG
    else:
        if set_debug:
            log_level: int = logging.DEBUG
        else:
            log_levels: list[int] = [logging.WARNING, logging.INFO, logging.DEBUG]
            ## Set log level based on verbosity counter
            log_level: int = log_levels[verbosity]

    logging.basicConfig(
        level=log_level,
        format=log_fmt_debug if verbosity == 2 else log_fmt,
        datefmt="%Y-%m-%d_%H-%M-%S",
    )

    logging.getLogger().setLevel(log_level)

    log.debug(f"Logging configured")


def parse_args() -> argparse.Namespace:
    """Handle CLI args for this script."""
    ## Initialize arg parser
    parser = argparse.ArgumentParser()

    ## Add debugging flag
    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="Enable debug logging"
    )
    ## Add verbosity counter
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        action="count",
        default=0,
        help="Increase verbosity level (-v, -vv, etc). Max verbosity: -vv",
    )

    options: argparse.Namespace = parser.parse_args()

    return options


def convert_bytes(
    bytes: int = None, as_obj: bool = False, as_str: bool = False
) -> t.Union[ConvertedBytes, str, int, float]:
    """Scale bytes up to proper unit (K, M, G, T, P).

    Params:
        bytes (int): Input bytes to convert up to proper unit.

    Example:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'

    """
    if as_obj and as_str:
        raise ValueError(
            f"Cannot pass both as_obj=True and as_str=True. Please use only 1 or the other."
        )

    factor: int = 1024

    for unit in VALID_FILESIZE_UNITS:
        if bytes < factor:
            if as_str:
                return f"{bytes:.2f}{unit}"
            elif as_obj:
                return ConvertedBytes(amount=Decimal(bytes), unit=unit)
            else:
                return round(bytes, 2)
        else:
            bytes /= factor


def get_cpu_count() -> int:
    """Return integer count of CPUs detected."""
    return multiprocessing.cpu_count()


def get_platform_terse() -> str:
    """Return 'terse' platform info."""
    return _platform.platform(terse=True)


def get_platform_aliased() -> str:
    """Return aliased platform info (may be the same as un-aliased)."""
    return _platform.platform(aliased=True)


def get_python_path() -> list[str]:
    """Return Python's PATH."""
    return sys.path


def get_python_modules() -> t.Dict[str, ModuleType]:
    """Return Python's loaded modules."""
    return sys.modules


def get_sys_byteorder() -> str:
    """Return "big" or "little.

    "big" for big-endian (most-significant byte first) platforms.
    "little" on little-endian (least-significant byte first) platforms.
    """
    return sys.byteorder


def get_os_release() -> dict[str, str]:
    """Return Linux OS release information."""
    match _platform.system():
        case "Linux" | "Unix":
            return get_freedesktop_release()
        case "Darwin":
            return EnumMac.VERSION.value
        case _:
            log.warning(
                f"Checking OS release on platform '{_platform.system()}' is not supported."
            )

            return None


def get_libc_version() -> t.Tuple[str]:
    """Return Unix system's libc version."""
    if _platform.system() not in ["Linux", "Unix", "Darwin"]:
        log.warning(
            f"Checking libc version on platform '{_platform.system()}' is not supported."
        )

        return None

    try:
        libc_ver = EnumUnix.LIBC_VER.value

        return libc_ver
    except Exception as exc:
        log.warning(f"({type(exc)}) Unable to detect libc version. Details: {exc}")

        return None


def get_freedesktop_release() -> dict[str, str] | None:
    """Return Linux freedesktop version."""
    match _platform.system():
        case "Unix" | "Linux":
            return _platform.freedesktop_os_release()
        case _:
            log.warning(
                f"Getting freedesktop release on OS '{_platform.system()}' is not supported."
            )

            return None
