#!/usr/bin/env python

from setuptools import setup

setup(name='DOMdiff',
      version='1.0',
      description=('Tool that, given two HTML pages, returns sub-trees of the'
                   'DOM that got removed and added, respectively.'),
      author='specialchar',
      author_email='specialchar@riseup.net',
      license='GPLv3',
      url='https://github.com/OpenMediaMonitor/domdiff',
      packages=['domdiff'],
      install_requires=[
          'beautifulsoup4>4.5,<5',
      ],
      tests_requires=[
          'pytest>3,<4',
      ]
     )
