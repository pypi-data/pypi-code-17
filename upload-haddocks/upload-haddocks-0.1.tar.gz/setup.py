#!/usr/bin/env python
############################################################
#
# setup
# Copyright (C) 2017, Richard Cook
# Released under MIT License
# https://github.com/rcook/upload-haddocks
#
############################################################

from __future__ import print_function
from setuptools import find_packages, setup

setup(
    name="upload-haddocks",
    version="0.1",
    description="Fix up Stack-generated Haskell documentation and upload it to Hackage",
    setup_requires=["setuptools-markdown"],
    long_description_markdown_filename="README.md",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    url="https://github.com/rcook/upload-haddocks",
    author="Richard Cook",
    author_email="rcook@rcook.org",
    license="MIT",
    packages=find_packages(),
    install_requires=["pyprelude"],
    include_package_data=True,
    test_suite="upload_haddocks.tests.suite",
    zip_safe=False)
