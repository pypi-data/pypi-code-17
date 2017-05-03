#!/usr/bin/env python3
from setuptools import setup
from findbig import __version__


setup(name='findbig',
      version=__version__,
      description='Command-line tool for finding the biggest files in a directory tree',
      url='http://gitlab.davepedu.com/dave/findbig',
      author='dpedu',
      author_email='dave@davepedu.com',
      packages=['findbig'],
      entry_points={
          "console_scripts": [
              "findbig = findbig.cli:main"
          ]
      })
