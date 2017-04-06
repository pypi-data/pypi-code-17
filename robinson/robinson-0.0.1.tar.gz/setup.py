#!/usr/bin/env python
"""Robinson install script"""

import os
import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import robinson

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

# long description from the relevant file
with codecs.open(os.path.join(SCRIPT_PATH, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='robinson',
    version=robinson.__version__,
    packages=['robinson', ],
    license='MIT',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/JiefeiC/robinson',
    author='JiefeiC',
    author_email='jiefei.chen@gmail.com',
)
