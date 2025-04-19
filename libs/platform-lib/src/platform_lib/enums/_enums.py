from __future__ import annotations

from enum import Enum
import platform as _platform
import typing as t

__all__ = ["EnumSystemTypes", "EnumMac", "EnumWin32", "EnumUnix"]


class EnumSystemTypes(Enum):
    """Enumerate options for platform.uname().system."""

    LINUX: str = "Linux"
    MAC: str = "Darwin"
    WINDOWS: str = "Windows"
    JAVA: str = "Java"


class EnumMac(Enum):
    """Mac-specific platform info."""

    VERSION: t.Tuple[str] = _platform.mac_ver()


class EnumWin32(Enum):
    """Windows-spectific platform info."""

    VERSION: t.Tuple[str] = _platform.win32_ver()
    EDITION: str = _platform.win32_edition()
    IS_IOT: bool = _platform.win32_is_iot()


class EnumUnix(Enum):
    LIBC_VER: t.Tuple[str] = _platform.libc_ver()
