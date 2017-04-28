#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'subcommands',
    version = 'v2.0',
    keywords = ('subcommands', 'egg'),
    description = 'Call system commands more conveniently.',
    license = 'MIT License',

    url = 'https://github.com/zhuangchaoxi/subcommands',
    author = 'zhuangchaoxi',
    author_email = 'zhuangchaoxi@kaike.la',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)
