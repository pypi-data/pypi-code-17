#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Top-level module for librosa"""

import warnings
import re
from .version import version as __version__

# And all the librosa sub-modules
import cache
import core
import beat
import decompose
import effects
import feature
import filters
import onset
import output
import segment
import util

# Exporting exception classes at the top level
from .util.exceptions import *  # pylint: disable=wildcard-import

# Exporting all core functions is okay here: suppress the import warning
from .core import *  # pylint: disable=wildcard-import

warnings.filterwarnings('always',
                        category=DeprecationWarning,
                        module='^{0}'.format(re.escape(__name__)))
