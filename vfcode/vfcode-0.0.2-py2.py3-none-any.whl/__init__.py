# -*- coding: utf-8 -*-

#                 _|_|                            _|
# _|      _|    _|        _|_|_|    _|_|      _|_|_|    _|_|
# _|      _|  _|_|_|_|  _|        _|    _|  _|    _|  _|_|_|_|
#   _|  _|      _|      _|        _|    _|  _|    _|  _|
#     _|        _|        _|_|_|    _|_|      _|_|_|    _|_|_|

"""
Anti-recognition verification code generation.

usage:

:copyright: (c) 2016 by xin053.
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = 'vfcode'
__version__ = '0.0.2'
__build__ = 0x000002
__author__ = 'xin053'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 xin053'


from .config import Config
from .generator import Generator
from . import render
from . import utils


# TODO 最后在整理需要在init中import哪些类
