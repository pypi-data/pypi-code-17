#!/usr/bin/env python
from setuptools import setup

setup(
	name='microquest',
	version='0.1.8',
	description='microquest - gamify anything - a cli alternative to liferpg / habitica',
	url='http://github.com/trqx/microquest',
	author='trqx',
	author_email='trqx@goat.si',
	license='MIT',
	packages=['microquest'],
	zip_safe=False,
	entry_points={
		'console_scripts': ['mq=microquest.mq:main']
	},
	install_requires=[
		'appdirs',
		'python-dateutil',
		'humanize',
		'tailer',
		'tabulate',
		'argcomplete'	
	],
	include_package_data=True
)
