#!/usr/bin/env python3

import sys
from .Start import *
# from Start import *

__title__ = 'BrosHelp'
__version__ = '0.0.1'
__author__ = 'Kay'
__license__ = 'MIT'
__copyright__ = '2017, Kay'
version_details = 'BrosHelp {ver} from {path} (python {pv.major}.{pv.minor}.{pv.micro})'.format(
    ver=__version__, path=__path__[0], pv=sys.version_info)
