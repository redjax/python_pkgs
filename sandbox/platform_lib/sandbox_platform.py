from __future__ import annotations

import logging

import platform_lib

log = logging.getLogger(__name__)

if __name__ == "__main__":
    platform_info: platform_lib.PlatformInfo = platform_lib.get_platform_info()
    platform_info.display_info()
