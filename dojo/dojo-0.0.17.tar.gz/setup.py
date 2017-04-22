#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo',
    version='0.0.17',
    description='A framework for building and running your Data platform',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo', 'dojo.adapters'],
    scripts=[],
    install_requires=[
        'pyyaml',
        'simplejson',
        'luigi==2.6.0'
    ]
)
