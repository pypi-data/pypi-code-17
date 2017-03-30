from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'CloudshellController',
  packages = find_packages(exclude=['contrib', 'docs', 'tests']), # this must be the same as the name above
  version = '0.6',
  description = 'Quali API Wrapper',
  long_description=long_description,
  author = 'Joe Auby',
  author_email = 'joeyauby@gmail.com',
  url = 'https://github.com/Madslick/CloudshellController', # use the URL to the github repo
  license='MIT',
  keywords = ['cloudshell', 'Quali', 'pypi', 'package'], # arbitrary keywords
  classifiers = [
  'Development Status :: 3 - Alpha', 
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent',
  'Programming Language :: Python',
  'Programming Language :: Python :: 2',
  'Programming Language :: Python :: 2.7',
  ],
  install_requires=['cloudshell-automation-api'],
  data_files=[('my_data', ['data/data_file'])]

)