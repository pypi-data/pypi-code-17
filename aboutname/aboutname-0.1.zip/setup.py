# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
setup(
  name = 'aboutname',
  packages = ['aboutname'], # this must be the same as the name above
  version = '0.1',
  description = 'know your name meaning',
  author = 'Umesh',
  author_email = 'kumar886umesh@gmail.com',
  url = 'https://github.com/umeshdhakar/name-meaning', # use the URL to the github repo
  keywords = ['name', 'meaning'], # arbitrary keywords
  classifiers = [],
)
