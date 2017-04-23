#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='logerator',
    version='0.3',
    description="A Python package that contains the decorator, before_and_after. The decorator implements before and after event logging using the Python Logentries package.",
    author="Bob Reselman",
    author_email='reselbob@gmail.com',
    url='https://github.com/reselbob/logerator',
    download_url='https://github.com/reselbob/logerator/archive/0.1.tar.gz',
    packages=['logerator'],
    install_requires=[
        'jsonpickle','logentries'
    ],
    package_dir={'logerator': 'logerator'},
    license="MIT license",
    keywords=['logerator', 'logging', 'logentries'],
    test_suite='tests'
)
