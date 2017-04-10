#!/usr/bin/env python

from __future__ import with_statement

import sys

from setuptools import setup

with open('README.rst') as readme:
    readme = readme.read()

if sys.version_info < (3, 4, 4):
    raise RuntimeError(
        'Installation requires Python 3.4.4+ (aiohttp/asyncio)')

setup(
    name = 'tecthulhu',
    version = '1.0',

    description = 'Python Tecthulhu',
    long_description = readme,
    author = 'Terence Honles',
    author_email = 'terence@honles.com',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],

    py_modules = ['tecthulhu'],
    package_dir = {'': 'src'},

    install_requires = [
        'aiohttp>=2.0',
    ],
)
