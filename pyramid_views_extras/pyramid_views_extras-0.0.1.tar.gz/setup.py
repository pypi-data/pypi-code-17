# -*- coding: utf-8 -*-

import os.path as osp
from setuptools import setup, find_packages

this_dir = osp.abspath(osp.dirname(__file__))

try:
    README = open(osp.join(this_dir, 'README.md'), 'r').read()
except IOError:
    README = ''

try:
    CHANGES = open(osp.join(this_dir, 'CHANGES.md'), 'r').read()
except IOError:
    CHANGES = ''

try:
    REQUIREMENTS = open(osp.join(this_dir, 'requirements.txt'), 'r').read().splitlines()
except IOError:
    REQUIREMENTS = []


def find_tests():
    import unittest

    loader = unittest.TestLoader()
    return loader.discover('pyramid_view_extras', pattern='tests.py')


setup(
    name='pyramid_views_extras',
    version='0.0.1',
    description='Additional view-related stuff for the Pyramid framework',
    long_description='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages(),
    test_suite='setup.find_tests',
    install_requires=REQUIREMENTS,
    author='Andriy Mykulyak',
    author_email='mykulyak@gmail.com',
    license='MIT',
)
