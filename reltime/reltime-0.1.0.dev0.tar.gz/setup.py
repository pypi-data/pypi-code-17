from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='reltime',
      version=version,
      description="find and normalize time information in unstructured text",
      long_description="""\
the reltime package uses regular expressions to identify common ways of speaking about dates and times in unstructred text,  as well as to normalize those dates and times into a standard format with the addition of a base date/time for the text.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords= ['relative', 'time', 'normalize', 'text', 'date'],
      author='Mark Brenckle',
      author_email='mark@liveapp.com',
      url='http://live.xyz',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      download_url = 'https://github.com/calendreco/reltime/archive/v0.1.tar.gz',
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'datetime',
          'python-dateutil'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
