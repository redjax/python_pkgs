from __future__ import annotations

from dataclasses import dataclass, field
import platform as _platform
import sys
from types import ModuleType
import typing as t

from platform_lib.classes.mixins import DictMixin
from platform_lib.enums._enums import EnumSystemTypes
from platform_lib.helpers import (
    get_cpu_count,
    get_libc_version,
    get_platform_aliased,
    get_platform_terse,
    get_python_modules,
    get_python_path,
    get_sys_byteorder,
)

__all__ = [
    "PlatformUnameBase",
    "PlatformSpecificInfoBase",
    "PlatformPythonBase",
    "PlatformInfoBase",
    "PlatformUnixInfoBase",
    "PlatformWinInfo",
    "PlatformMacInfo",
]


@dataclass
class PlatformUnameBase(DictMixin):
    system: str = _platform.uname().system
    node: str = _platform.uname().node
    release: str = _platform.uname().release
    version: str = _platform.uname().version
    machine: str = _platform.uname().machine


@dataclass
class PlatformSpecificInfoBase(DictMixin):
    """Base class for platform-specific (i.e. Windows, Mac, Linux) info.

    Description:
        Some of the platform module's functions are only available when a
        specific platform is detected. This class serves as a base for
        platform-specific "extra" data.

    """

    os: str = field(default_factory=_platform.system)


@dataclass
class PlatformPythonBase(DictMixin):
    """Information about the Python implementation for the platform."""

    build: t.Tuple[str, str] = field(default_factory=_platform.python_build)
    compiler: str = field(default_factory=_platform.python_compiler)
    branch: str = field(default_factory=_platform.python_branch)
    implementation: str = field(default_factory=_platform.python_implementation)
    revision: str = field(default_factory=_platform.python_revision)
    version: str = field(default_factory=_platform.python_version)
    version_tuple: t.Tuple[str, str, str] = field(
        default_factory=_platform.python_version_tuple
    )
    path: t.List[str] = field(default_factory=get_python_path)
    modules: t.Dict[str, ModuleType] = field(default_factory=get_python_modules)
    base_prefix: str = field(default=sys.base_prefix)
    exec_prefix: str = field(default=sys.exec_prefix)
    copyright: str = field(default=sys.copyright)
    dont_write_bytecode: bool = field(default=sys.dont_write_bytecode)
    executable: str = field(default=sys.executable)
    flags: t.Tuple[t.Union[int, bool]] = field(default=sys.flags)
    float_info: t.Tuple[t.Union[int, float]] = field(default=sys.float_info)
    default_encoding: str = field(default_factory=sys.getdefaultencoding)
    int_max_str_digits: int = field(default_factory=sys.get_int_max_str_digits)
    recursion_limit: int = field(default_factory=sys.getrecursionlimit)
    maxsize: int = field(default=sys.maxsize)
    maxunicode: int = field(default=sys.maxunicode)


@dataclass
class PlatformUnixInfoBase(DictMixin):
    """Unix-specific platform info."""

    libc_ver: t.Tuple[str] = field(default=get_libc_version)


@dataclass
class PlatformInfoBase(DictMixin):
    """Base class for platform information.

    Description:
        Compile platform data common across all OSes to serve as a base for
        building platform-specific classes.
    """

    platform: str = field(default_factory=_platform.platform)
    platform_terse: str = field(default=get_platform_terse)
    platform_aliased: str = field(default=get_platform_aliased)
    machine: str = field(default_factory=_platform.machine)
    system: str = field(default_factory=_platform.system)
    release: str = field(default_factory=_platform.release)
    version: str = field(default_factory=_platform.version)
    processor: str | None = field(default_factory=_platform.processor)
    cpu_count: int = field(default_factory=get_cpu_count)
    arch: t.Tuple[str, str] = field(default_factory=_platform.architecture)
    byteorder: str = field(default_factory=get_sys_byteorder)

    def is_linux(self) -> bool:
        if self.system == EnumSystemTypes.LINUX.value:
            return True
        else:
            return False

    def is_unix(self) -> bool:
        if self.system in [EnumSystemTypes.LINUX.value, EnumSystemTypes.MAC.value]:
            return True
        else:
            return False

    def is_win(self) -> bool:
        if self.system == EnumSystemTypes.WINDOWS.value:
            return True
        else:
            return False

    def is_mac(self) -> bool:
        if self.system == EnumSystemTypes.MAC.value:
            return True
        else:
            return False

    def is_java(self) -> bool:
        if self.system == EnumSystemTypes.JAVA.value:
            return True
        else:
            return False

    def is_32bit(self) -> bool:
        if "32bit" in self.arch:
            return True
        else:
            return False

    def is_64bit(self) -> bool:
        if "64bit" in self.arch:
            return True
        else:
            return False
