#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'future',
    'python-dateutil',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='odootools',
    version='0.1.0',
    description="Package that conatin some tools to simplify Odoo addons developpement",
    long_description=readme + '\n\n' + history,
    author="Mohamed Cherkaoui",
    author_email='chermed@gmail.com',
    url='https://github.com/chermed/odootools',
    packages=[
        'odootools',
    ],
    package_dir={'odootools':
                 'odootools'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='odootools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
