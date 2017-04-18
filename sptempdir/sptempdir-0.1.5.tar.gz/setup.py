# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from sptempdir import __version__, __git_url__


try:
	with open('PYPI_README.rst', 'r') as f:
		pypi_web_description = f.read()
except Exception as e:
	pypi_web_description = ''

setup(
	name='sptempdir',

	# https://packaging.python.org/en/latest/distributing.html#version
	version=__version__,

	keywords=['tempdir', 'sptempdir', 'temporary directory', 'directory', 'temporary'],
	description='This module generates temporary directories',
	long_description=pypi_web_description,

	# The project homepage
	url=__git_url__,

	# Author details
	author='Ales Krejci',
	author_email='aleskrejcicz@gmail.com',

	packages=find_packages(exclude=['docs', 'tests']),
	include_package_data=True,
	license="BSD",
	platforms='any',

	# https://packaging.python.org/en/latest/distributing.html#classifiers
	classifiers=[
		# License:
		'License :: OSI Approved :: BSD License',

		# Python versions:
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	]
)
