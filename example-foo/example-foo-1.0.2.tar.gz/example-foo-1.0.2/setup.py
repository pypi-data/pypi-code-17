#!/usr/bin/env python

from setuptools import setup

setup(
    author='Doug Beck',
    author_email='doug@douglasbeck.com',
    name='example-foo',
    version='1.0.2',
    url='https://github.com/beck/sandbox/tree/example-foo',
    install_requires=[
        'example-bar == 1.0.1'
    ]
)
