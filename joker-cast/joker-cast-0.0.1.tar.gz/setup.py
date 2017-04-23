#!/usr/bin/env python3
# coding: utf-8

import os
import re

from setuptools import setup, find_packages


# import joker; exit(1)
# DO NOT import your package from your setup.py


def readfile(filename):
    with open(filename) as f:
        return f.read()


# change this
package_name = 'cast'
description = 'Some type conversion utilities'


def getversion():
    root = os.path.dirname(__file__)
    path = os.path.join(root, 'joker/{}/VERSION'.format(package_name))
    with open(path) as version_file:
        version = version_file.read().strip()
        regex = re.compile(r'^\d+\.\d+\.\d+$')
        if not regex.match(version):
            raise ValueError('VERSION file is corrupted')
        return version


config = {
    'name': "joker-" + package_name,
    'version': getversion(),
    'description': '' + description,
    'keywords': '',
    'url': "https://github.com/frozflame/joker-cast",
    'author': 'frozflame',
    'author_email': 'frozflame@outlook.com',
    'license': "GNU General Public License (GPL)",
    'packages': find_packages(exclude=['test_*']),
    'namespace_packages': ["joker"],
    'zip_safe': False,
    'install_requires': readfile("requirements.txt"),
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # ensure copy static file to runtime directory
    'include_package_data': True,
}

setup(**config)
