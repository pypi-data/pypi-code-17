# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.std.typing',
    version_info=(0, 1, 0),
    __version__='0.1.0',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='wrapper to handle dependency differences between version, and missing Text in 3.5.0/1',  # NOQA
    # keywords="",
    entry_points=None,
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    install_requires=dict(
        any=[],
        py27=['typing'],
        py33=['typing'],
        py34=['typing'],
    ),
    license='MIT License',
    universal=True,
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

###########

import sys              # NOQA
import typing           # NOQA
from typing import *    # NOQA

if (3, 5, 0) <= sys.version_info < (3, 5, 2):
    Text = str
