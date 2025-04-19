from __future__ import annotations

import argparse

from platform_lib.classes.platform import PlatformInfo, get_platform_info

def main(options: argparse.Namespace):
    platform_info: PlatformInfo = get_platform_info()

    if options.debug:
        print(platform_info.ascii_art)
        print()
        print(platform_info)

    else:

        if options.verbosity == 0 or options.verbosity is None:

            msg: str = f"""[ Platform Info ]
    OS: {platform_info.system}
    CPU: {platform_info.processor} ({platform_info.cpu_count} core(s))
    Python: {platform_info.python.implementation} v{platform_info.python.version} ({platform_info.python.exec_prefix})
    """
            print(msg)

        if options.verbosity == 1:
            print(platform_info.ascii_art)
            print()

            platform_info.display_info(simplified=True)

        elif options.verbosity >= 2:
            print(platform_info.ascii_art)
            print()

            platform_info.display_info(simplified=False)
