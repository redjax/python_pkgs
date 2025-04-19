from __future__ import annotations

from dataclasses import dataclass, field
import logging
import typing as t

from platform_lib.classes.base import (
    PlatformInfoBase,
    PlatformPythonBase,
    PlatformSpecificInfoBase,
    PlatformUnameBase,
    PlatformUnixInfoBase,
)
from platform_lib.classes.spinners import CLISpinner
from platform_lib.enums._enums import EnumSystemTypes, EnumWin32
from platform_lib.helpers import get_os_release
from platform_lib.methods import get_os_ascii

log = logging.getLogger(__name__)

__all__ = [
    "PlatformUname",
    "PlatformPython",
    "PlatformWinInfo",
    "PlatformMacInfo",
    "PlatformLinuxInfo",
    "PlatformInfo",
    "get_platform_python",
    "get_platform_info",
    "get_platform_uname",
]


def get_platform_uname() -> "PlatformUname":
    """Return an initalized PlatformUname instance."""
    return PlatformUname()


def get_platform_python() -> "PlatformPython":
    """Return an initalized PlatformPython instance."""
    return PlatformPython()


@dataclass
class PlatformUname(PlatformUnameBase):
    pass


@dataclass
class PlatformPython(PlatformPythonBase):
    """Information about the Python implementation for the platform."""

    pass


@dataclass
class PlatformSpecificInfo(PlatformSpecificInfoBase):
    """Base class for platform-specific (i.e. Windows, Mac, Linux) info.

    Description:
        Some of the platform module's functions are only available when a
        specific platform is detected. This class serves as a base for
        platform-specific "extra" data.

    """

    pass


@dataclass
class PlatformWinInfo(PlatformSpecificInfo):
    """Windows-specific platform info."""

    win32_ver: t.Tuple = field(default=EnumWin32.VERSION.value)
    win32_edition: str = field(default=EnumWin32.EDITION.value)
    win32_is_iot: bool = field(default=EnumWin32.IS_IOT.value)


@dataclass
class PlatformMacInfo(PlatformUnixInfoBase):
    """Mac-specific platform info."""

    mac_ver: t.Tuple[str] = field(default=get_os_release)


@dataclass
class PlatformLinuxInfo(PlatformUnixInfoBase):
    """Linux-specific platform info."""

    os_release: dict[str, str] = field(default_factory=get_os_release)


@dataclass
class PlatformInfo(PlatformInfoBase):
    """Compile information about the OS running this script."""

    uname: PlatformUnameBase = field(default_factory=get_platform_uname)
    python: PlatformPythonBase = field(default_factory=get_platform_python)

    @property
    def platform_specific_info(
        self,
    ) -> t.Union[PlatformWinInfo, PlatformMacInfo, PlatformMacInfo]:
        """Detect OS and return platform-specific class with additional platform info."""
        match self.system:
            case EnumSystemTypes.LINUX.value:
                platform_extra: PlatformLinuxInfo = PlatformLinuxInfo()
            case EnumSystemTypes.WINDOWS.value:
                platform_extra: PlatformWinInfo = PlatformWinInfo()
            case EnumSystemTypes.MAC.value:
                platform_extra: PlatformMacInfo = PlatformMacInfo()
            case _:
                log.error(f"Unknown OS: {self.system}")

                return f"<UNKNOWN_OS:'{self.system}'>"

        return platform_extra

    @property
    def ascii_art(self) -> str:
        _ascii: str = get_os_ascii(os=self.system)

        return _ascii

    def display_info(self, simplified: bool = True):
        if simplified:
            msg: str = f"""[ Platform Information ]
OS:
    Type: {self.system}
    Release: {self.release}
    Version: {self.version}
    Hostname: {self.uname.node}
    Kernel release: {self.uname.release}
CPU Architecture:
    x86/x64: {self.processor}
    CPU count: {self.cpu_count}
Python:
    Version: {self.python.version}
    Executable location: {self.python.exec_prefix}
    Default encoding: {self.python.default_encoding}
    'PYTHONDONTWRITEBYTECODE' environment variable: {self.python.dont_write_bytecode}
"""

        else:

            msg: str = f"""[ Platform Information ]
OS:
    Type: {self.system}
    Release: {self.release}
    Version: {self.version}
    Platform: {self.platform}
    Uname:
        Node (hostname): {self.uname.node}
        Kernel release: {self.uname.release}
CPU Architecture:
    x86/x64: {self.processor}
    CPU count: {self.cpu_count}
Python:
    Implementation: {self.python.implementation}
    Version: {self.python.version}
    Executable location: {self.python.exec_prefix}
    Base prefix: {self.python.base_prefix}
    Build: {self.python.build}
    Revision: {self.python.revision}
    Compiler: {self.python.compiler}
    Flags: {self.python.flags}
    Default encoding: {self.python.default_encoding}
    'PYTHONDONTWRITEBYTECODE' environment variable: {self.python.dont_write_bytecode}

"""

        print(msg)


def get_platform_info() -> PlatformInfo:
    """Entrypoint for platform info class.

    Description:
        This method initializes a `PlatformInfo` object, handling any exceptions
        and returning a PlatformInfo class where possible.
    """
    with CLISpinner(message="Compiling platform information... "):
        try:
            p_info: PlatformInfo = PlatformInfo()

            return p_info
        except Exception as exc:
            msg = f"({type(exc)}) Unhandled exception initializing PlatformInfo object. Details: {exc}"
            log.error(msg)

            raise exc
