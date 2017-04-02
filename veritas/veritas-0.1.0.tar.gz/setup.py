#!/usr/bin/env python

import os
import re
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


readme = open('README.rst').read()

def get_version():
    VERSIONFILE = os.path.join('veritas', '__init__.py')
    VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(VERSIONFILE, 'rt').read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name="veritas",
    version=get_version(),
    description="an executable implementation of _ in function definitions",
    long_description=readme,
    license="BSD",
    author="lonnen",
    url='https://github.com/lonnen/veritas',
    packages=find_packages(),
    install_requires=[],
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
