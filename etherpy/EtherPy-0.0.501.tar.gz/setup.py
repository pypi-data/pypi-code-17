#!/usr/bin/env python

from setuptools import setup

setup(name='EtherPy',
      version='0.0.501',
      description='Python Ethereum Node Client',
      author='Chip Wasson',
      author_email='chip@wasson.io',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['etherpy'],
      package_dir={'etherpy': 'src/etherpy'},
      )
