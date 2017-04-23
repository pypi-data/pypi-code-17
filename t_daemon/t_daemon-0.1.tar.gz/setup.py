#!/usr/bin/env python

from setuptools import setup

setup(name = 't_daemon',
      version = '0.1',
      description = 'T daemon library',
      url = 'https://gitlab.com/ddmello/lib/python/t_daemon.git',
      author = 'Darrin D\'Mello',
      author_email = 'darrin.dmello@gmail.com',
      license = 'MIT',
      packages = ['t_daemon'],
      install_requires = [
         't_io',
         't_logging',
         't_process'
      ],
      zip_safe = True)
