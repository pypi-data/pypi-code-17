#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Copyright (c) since 2016, CESNET, z. s. p. o.
# Authors: Pavel Kácha <pavel.kacha@cesnet.cz>
#          Jan Mach <jan.mach@cesnet.cz>
# Use of this source is governed by an ISC license, see LICENSE file.
#-------------------------------------------------------------------------------

# Resources:
#   https://packaging.python.org/en/latest/
#   http://python-packaging-user-guide.readthedocs.io/distributing/

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'typedcols',
    version = '0.1.7',
    description = 'Python library providing typed collections.',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
    ],
    keywords = 'library',
    url = 'https://homeproj.cesnet.cz/git/idea.git',
    author = 'Pavel Kacha',
    author_email = 'pavel.kacha@cesnet.cz',
    license = 'ISC',
    py_modules = ['typedcols'],
    test_suite = 'nose.collector',
    tests_require = [
        'nose'
    ],
    zip_safe = True
)
