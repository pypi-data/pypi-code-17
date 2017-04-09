#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path
from hannakageul import __version__

here = path.abspath(path.dirname(__file__))
packages = find_packages(exclude=['build', '_docs', 'VENV'])

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hannakageul',
    version=__version__,
    description='Hangeul - Kana encoding converter',
    long_description=long_description,
    author='Mirai Kim',
    author_email='nachtbeere@outlook.com',
    license='MIT',
    url='https://github.com/noxowl/hannakageul',
    keywords=['charset','encoding','converter','euc-kr','shift-jis'],
    packages=packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Korean',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3.5'
    ]
    )
