# -*- coding: utf-8 -*-
try:
	import setuptools
	from setuptools import setup, find_packages
except ImportError:
	print("Please install setuptools.")

import os
long_description = 'oracle tools: carefully acccess, etc. by anad labo..'
if os.path.exists('README.txt'): long_description = open('README.txt').read()
setup(
	name  = 'oracler',
	version = '0.0.3',
	description = 'oracle tools: carefully acccess, etc.',
	long_description = long_description,
	license = 'MIT',
	author = 'dais.cns@gmail.com',
	author_email = 'dais.cns@gmail.com',
	url = 'https://anad.site/',
	keywords = 'oracle tools develop coding',
	packages = find_packages(),
	install_requires = ['PyYAML', ],
	classifiers = [
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'Programming Language :: Python :: 3.5'
	]
)
'''
公開
まずPyPI > Registerでアカウントを作成します。次に下記のコマンドを実行します。
# PyPIアカウントでログイン
$ python3 setup.py register

# register.pyを作成している場合
$ python3 register.py

# 作成していない場合
$ python3 setup.py sdist upload
'''
