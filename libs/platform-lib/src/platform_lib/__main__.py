from __future__ import annotations

import logging

from platform_lib.helpers import _set_logging_level, parse_args
from platform_lib.main import main

log = logging.getLogger(__name__)

if __name__ == "__main__":
    args = parse_args()

    _set_logging_level(verbosity=args.verbosity, set_debug=args.debug)

    main(options=args)
