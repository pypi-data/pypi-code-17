#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='wordstop',
    version='0.0.1',
    description='Word frequency counter',
    author='Viet Hung Nguyen',
    author_email='hvn@familug.org',
    py_modules=['wordstop'],
    url='https://github.com/hvnsweeting/wordstop',
    entry_points='''[console_scripts]
        wordstop=wordstop:cli
    '''
)
