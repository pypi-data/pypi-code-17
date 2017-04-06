#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'xmltodict',
]

test_requirements = [
    'bumpversion'
    'flake8',
    'tox',
    'Sphinx',
    'PyYAML',
    'pytest',
]

setup(
    name='postalcodes-mexico',
    version='0.1.0',
    description="Determine large parts of a Mexican postal address from its postal code (C.P.).",
    long_description=readme + '\n\n' + history,
    author="Florian Posdziech",
    author_email='hallo@flowfx.de',
    url='https://github.com/flowfx/postalcodes_mexico',
    packages=['postalcodes-mexico',],
    package_dir={'postalcodes-mexico':
                 'postalcodes_mexico'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords=['postal code', 'mexico', 'address'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
