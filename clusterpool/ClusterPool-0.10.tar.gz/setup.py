#!/usr/bin/env python

from distutils.core import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='ClusterPool',
      version='0.10',
      description='Allows mapping over large lists of objects with a calculate() function on a supercomputer cluster',
      author='Joseph Goodknight',
      author_email='joey.goodknight@gmail.com',
      url='https://github.com/jgoodknight/ClusterPool/',
      long_description=long_description,
      license="MIT",
      packages=['ClusterPool'],
      package_dir = {'ClusterPool': 'src'} ,
      package_data={'ClusterPool': ['GENERAL/*.template', 'SLURM/*.template']})
