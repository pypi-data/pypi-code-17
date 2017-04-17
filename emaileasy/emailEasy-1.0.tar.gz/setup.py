#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'emailEasy',
    version = 'v1.0',
    keywords = ('emailEasy', 'egg'),
    description = 'Make email easier.',
    license = 'MIT License',

    url = 'https://github.com/zhuangchaoxi/easyEmail',
    author = 'zhuangchaoxi',
    author_email = 'zhuangchaoxi@kaike.la',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)
