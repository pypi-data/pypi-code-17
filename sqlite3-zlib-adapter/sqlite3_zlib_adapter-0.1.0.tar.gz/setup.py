#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sqlite3_zlib_adapter',
    version='0.1.0',
    description="sqlite3_zlip_adapter is a custom class with adapter and convert function to store strings into a SQLite column as zlib blobs.",
    long_description=readme + '\n\n' + history,
    author="Miguel González",
    author_email='migonzalvar@gmail.com',
    url='https://github.com/migonzalvar/sqlite3_zlib_adapter',
    packages=[
        'sqlite3_zlib_adapter',
    ],
    package_dir={'sqlite3_zlib_adapter':
                 'sqlite3_zlib_adapter'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='sqlite3_zlib_adapter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
