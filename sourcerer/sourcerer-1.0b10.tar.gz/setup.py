#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [  # TODO: put package requirements here
]

test_requirements = [  # TODO: put package test requirements here
]

setup(name='sourcerer',
      version="1.0b10",
      author="Jonathan Ferretti",
      author_email="jon@jonathanferretti.com",
      description="Library to programatically genrate python source code",
      long_description=readme + '\n\n' + history,
      url='https://github.com/LISTERINE/sourcerer',
      packages=['sourcerer', ],
      package_dir={'sourcerer': 'sourcerer'},
      include_package_data=True,
      install_requires=['pyaml', 'yapf'],
      license="Apache2",
      zip_safe=False,
      keywords='sourcerer',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Natural Language :: English',
                   "Programming Language :: Python :: 2",
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4', ],
      test_suite='tests',
      tests_require=['pyaml', 'yapf'])
