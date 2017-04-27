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

# dynamic import
basedir = dirname(__file__)
__all__ = []
for name in glob(join(basedir, '*.py')):
    module = splitext(split(name)[-1])[0]
    if module in ['__main__', '__init__']:
        continue
    print(module)
    try:
        __import__('batchphoto.crop.' + module)
    except:
        warnings.warn('Exception while loading {}. Ignoring.\n'.format(module))
        traceback.print_exc()
    else:
        __all__.append(module)

__all__.sort()
