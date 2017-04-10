#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as readmefile:
	long_description = readmefile.read()
	
setup(name="F2python",
      version="1.5.0",
      scripts=['bootf2.py'],
      description="The F2 DBMS written in Python. Needs ZODB and ZEO to run.",
      author="Thibault Estier",
      author_email="thibault.estier@unil.ch",
      url="https://pypi.python.org/pypi/F2python/",
      packages=['F2'],
      install_requires=['ZODB3'],
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Topic :: Database :: Database Engines/Servers"
      ]
     )
