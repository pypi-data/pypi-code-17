#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import platform
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

def readme():
    try:
        return open('README.rst', encoding='utf-8').read()
    except TypeError:
        return open('README.rst').read()


setup(
    name='local-cname',
    packages=find_packages(),
    version='0.1',
    description='Local CNAME',
    long_description=readme(),
    author='henning@jacobs1.de',
    url='https://github.com/hjacobs/local-cname',
    keywords='dns hosts local',
    license='',
    setup_requires=['flake8'],
    install_requires=[],
    tests_require=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    entry_points={'console_scripts': ['local-cname = local_cname.cli:main']}
)
