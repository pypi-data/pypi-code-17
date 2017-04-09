# coding=utf-8
import os

from setuptools import find_packages
from setuptools import setup

setup(
    name = 'slideslurp',
    version = '0.0.3',
    description = 'SlideShare to PDF',
    author = 'Veit Heller',
    author_email = 'veit@veitheller.de',
    license = 'MIT License',
    url = 'https://github.com/hellerve/slideslurp',
    download_url = 'https://github.com/hellerve/slideslurp/tarball/0.0.3',
    packages = find_packages('.'),
    install_requires=[
        "bs4",
        "reportlab",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'slideslurp = slideslurp:main',
        ]
    },
    include_package_data = True,
)
