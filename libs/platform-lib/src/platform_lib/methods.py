import logging

from platform_lib import ascii_art

log = logging.getLogger(__name__)

__all__ = [
    "get_os_ascii",
]


def get_os_ascii(os: str) -> str | None:
    if os is None:
        return

    match os.lower():
        case "mac" | "darwin":
            _ascii: str = ascii_art.mac_ascii

        case "win32" | "windows":
            _ascii: str = ascii_art.win_ascii

        case "linux":
            _ascii: str = ascii_art.linux_ascii

        case "bsd":
            _ascii: str = ascii_art.bsd_ascii

        case _:
            _ascii: str = ascii_art.other_ascii

    return _ascii
