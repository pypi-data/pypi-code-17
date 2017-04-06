#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
	name='hahatest',
	version='0.0.6',
	license='http://www.apache.org/licenses/LICENSE-2.0',
	description=u'测试测试',
	author='heliang',
	author_email='heliang.whut@gmail.com',
	url='https://abc.xyz',
	packages=['hahatest'],
	install_requires=[],
	entry_points={
		'console_scripts': [
			'haha=hahatest:haha'
		]
	},
	classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
