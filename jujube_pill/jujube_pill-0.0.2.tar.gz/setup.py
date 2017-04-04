#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='jujube_pill',
    version='0.0.2',
    author='xlzd',
    author_email='xlzd',
    url='https://xx.c',
    description=u'吃枣药丸',
    packages=['jujube_pill'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=jujube_pill:jujube',
            'pill=jujube_pill:pill'
        ]
    }
)
