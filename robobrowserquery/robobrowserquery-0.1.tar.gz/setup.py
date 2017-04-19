#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from robobrowserquery import __author__, __version__, __license__

setup(
    name='robobrowserquery',
    version=__version__,
    description='PyQuery on RoboBrowser',
    license=__license__,
    author=__author__,
    author_email='ytyng@live.jp',
    url='https://github.com/ytyng/robobrowserquery.git',
    keywords='RoboBrowser, PyQuery, Browser, Scraping',
    packages=['robobrowserquery'],
    install_requires=['robobrowser', 'pyquery'],
    entry_points={
    },
)
