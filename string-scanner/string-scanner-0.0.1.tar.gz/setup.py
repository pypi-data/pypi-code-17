#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION_FILE = open('VERSION')
VERSION = VERSION_FILE.read().strip()


def readme():
    """Helper function for long_description"""
    with open('README.rst') as readme_file:
        return readme_file.read()


setup(
    name='string-scanner',
    version=VERSION,
    url='http://github.com/sanscore/py-string-scanner/',

    description='',
    long_description=readme(),
    keywords='',

    author='Grant Welch',
    author_email='gwelch925 at gmail.com',
    license='Apache License 2.0',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=[
        'regex',
    ],

    setup_requires=[
        'pytest-runner',
        'wheel',
    ],

    tests_require=[
        'pytest',
        'mock',
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
    ],

    include_package_data=True,
    zip_safe=False,
)
