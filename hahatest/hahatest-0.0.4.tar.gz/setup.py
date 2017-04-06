#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
	name='hahatest',
	version='0.0.4',
	author='heliang',
	author_email='heliang.whut@gmail.com',
	url='https://abc.xyz',
	description=u'测试测试',
	packages=['hahatest'],
	install_requires=[],
	entry_points={
		'console_scripts': [
			'haha=hahatest:haha'
		]
	}
)
