#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='dojo',
    version='0.0.19',
    description='A framework for building and running your Data platform',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    scripts=[],
    install_requires=[
        'pyyaml',
        'jsonschema',
        'python-dateutil'
    ]
)
