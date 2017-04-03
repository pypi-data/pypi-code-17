#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.3.3'

setup(
  name='google.foresite-toolkit',
  version=version,
  description='Library for constructing, parsing, manipulating and serializing OAI-ORE Resource Maps',
  long_description="""\
  """,
  classifiers=[],
  author='Rob Sanderson',
  author_email='azaroth@liv.ac.uk',
  url='http://code.google.com/p/foresite-toolkit/',
  license='BSD',
  packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
  include_package_data=True,
  zip_safe=False,

  # Specify additional patterns to match files and directories that may or may
  # not be matched by MANIFEST.in or found in source control.
  package_data = {
    '': ['*.txt'],
  },

  install_requires = [
    'rdflib == 4.2.2',
    'lxml == 3.7.3',
  ],

  test_suite='foresite.tests.test_suite'
)
