#!/usr/bin/env python

import sys

if sys.version_info[0] == 3:
    from LocalitySensitiveHashing.LocalitySensitiveHashing import __version__
    from LocalitySensitiveHashing.LocalitySensitiveHashing import __author__
    from LocalitySensitiveHashing.LocalitySensitiveHashing import __date__
    from LocalitySensitiveHashing.LocalitySensitiveHashing import __url__
    from LocalitySensitiveHashing.LocalitySensitiveHashing import __copyright__
    from LocalitySensitiveHashing.LocalitySensitiveHashing import LocalitySensitiveHashing
    from LocalitySensitiveHashing.LocalitySensitiveHashing import DataGenerator

else:
    from LocalitySensitiveHashing import __version__
    from LocalitySensitiveHashing import __author__
    from LocalitySensitiveHashing import __date__
    from LocalitySensitiveHashing import __url__
    from LocalitySensitiveHashing import __copyright__
    from LocalitySensitiveHashing import LocalitySensitiveHashing
    from LocalitySensitiveHashing import DataGenerator





