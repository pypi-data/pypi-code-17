#!/usr/bin/env python

from setuptools import setup

setup(name='hmc',
      version='0.3',
      description='Decision tree based hierachical multi-classifier',
      url='https://github.com/davidwarshaw/hmc',
      author='David Warshaw',
      author_email='david.warshaw@gmail.com',
      py_modules=['hmc.hmc', 'hmc.datasets', 'hmc.metrics', 'hmc.exceptions'],
      requires=['sklearn', 'numpy', 'pandas'])
