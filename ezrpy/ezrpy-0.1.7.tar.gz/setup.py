#!/usr/bin/env python
from setuptools import setup

setup(name='ezrpy',
      version='0.1.7',
      description='Automatic REST API for Prototypes',
      author='Marcelo Jara',
      author_email='marjara35@gmail.com',
      keywords=['rest', 'prototype', 'api'],
      url='https://github.com/mijara/ezrpy',
      packages=['ezrpy'],
      scripts=['scripts/ezt'],
      install_requires=[
          'flask',
          'tinydb',
          'requests',
      ])
