#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='dojo',
    version='0.0.20',
    description='A framework for building and running your Data platform',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    scripts=['bin/dojo'],
    install_requires=[
        'pyyaml',
        'jsonschema',
        'python-dateutil'
    ]
)
