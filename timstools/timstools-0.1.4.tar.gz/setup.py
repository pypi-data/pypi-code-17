from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
	long_description = f.read()
setup(
	name = 'timstools',
	# Versions should comply with PEP440. For a discussion on single-sourcing
	# the version across setup.py and the project code, see
	# https://packaging.python.org/en/latest/single_source_version.html
	version='0.1.4',
	description = 'Collection of tools for helping you program faster',
	long_description =long_description,
	# The project's main homepage.
	url = 'https://github.com/timeyyy/timstools',
	# Author details
	author='tmothy eichler',
	author_email='tim_eichler@hotmail.com',
	# Choose your license
	license='BSD3',
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	],

	# What does your project relate to?
	keywords = 'misc programming tools python3 general generic',

	packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)
