#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module flask_bluelogin
"""

__version_info__ = (0, 1, 0)
__version__ = '.'.join([str(val) for val in __version_info__])

__namepkg__ = "flask-bluelogin"
__desc__ = "Flask BlueLogin module"
__urlpkg__ = "https://github.com/fraoustin/flask-bluelogin.git"
__entry_points__ = {}

from flask_bluelogin.main import *
