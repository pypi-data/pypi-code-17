#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Module executor for ``climenu``.
'''

from __future__ import print_function
import os
from .version import __version__


if __name__ == '__main__':
    print("climenu version %s" % __version__)
    print("...running from %s" % os.path.dirname(__file__))
