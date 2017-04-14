#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Life's pathetic, happy coding ♡~ Nasy.

O._.O
(\=/)

@author: Nasy
@date: Apr 13, 2017
@email: sy_n@me.com
@file: setup.py
@license: MIT

Copyright © 2017 by Nasy. All Rights Reserved.
"""

import setuptools

import cqdb

f = open("requirements.txt", "rb")
REQUIRES = [i.strip() for i in f.read().decode("utf-8").split("\n")]

setuptools.setup(
    name="cqdb",
    version=cqdb.__version__,
    license="MIT LICENSE",
    # url="https://github.com/nasyxx/cqdb",
    author="Nasy",
    author_email="sy_n@me.com",
    description="My school db lib",
    long_description=(open('README.rst').read() + '\n' + open('AUTHORS.rst')
                      .read() + '\n' + open('HISTORY.rst').read() + '\n'),
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
