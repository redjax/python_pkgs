from __future__ import annotations

from platform_lib import script as platform_script

if __name__ == "__main__":
    args = platform_script.get_args()

    platform_script._set_logging_level(verbosity=args.verbosity, set_debug=args.debug)

    platform_script.main(options=args)
