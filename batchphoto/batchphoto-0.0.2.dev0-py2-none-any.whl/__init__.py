# -*- coding: utf-8 -*-
# Batchphoto
#
# Copyright (c) 2017 Justin Weber
# Licensed under the terms of the MIT License
# see LICENSE

# Import from the future for Python 2 and 3 compatability!
from __future__ import print_function, absolute_import, unicode_literals
from glob import glob
from os.path import dirname, join, split, splitext
import warnings
import traceback

version_info = (0, 0, 2, "dev0")

__version__ = '.'.join(map(str, version_info))
__license__ = 'Licensed under the terms of the MIT License'
__project_url__ = 'https://github.com/onlyjus/batchphoto'

# dynamic import
basedir = dirname(__file__)
__all__ = []
for name in glob(join(basedir, '*/__init__.py')):
    dir_ = dirname(name)
    module = splitext(split(dir_)[-1])[0]
    try:
        __import__('batchphoto.' + module)
    except:
        warnings.warn('Exception while loading {}. Ignoring.\n'.format(module))
        traceback.print_exc()
    else:
        __all__.append(module)

__all__.sort()
