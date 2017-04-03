#!/usr/bin/env python3

import codecs
import os
import setuptools

FILEPATH = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(FILEPATH, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='doxybuild',
    version='0.1-alpha',
    description='Scripts for building documents in Doxy',
    long_description=LONG_DESCRIPTION,
    url='https://gitlab.com/doxy/doxybuild/',
    author='Alex Thorne',
    author_email='alex@thorne.cc',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=['doxycore'],
    scripts=['doxybuild.py'],
    keywords=['ci', 'doxy', 'tex', 'latex', 'document'],
)
