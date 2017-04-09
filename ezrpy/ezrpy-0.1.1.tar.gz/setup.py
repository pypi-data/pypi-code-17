#!/usr/bin/env python
from distutils.core import setup

setup(name='ezrpy',
      version='0.1.1',
      description='Automatic REST API for Prototypes',
      author='Marcelo Jara',
      author_email='marjara35@gmail.com',
      keywords=['rest', 'prototype', 'api'],
      url='https://github.com/mijara/ezrpy',
      packages=['ezrpy'],
      install_requires=[
          'flask',
      ],
      )
