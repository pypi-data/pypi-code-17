# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-grafico-db',
	version='1.0',
	license='BSD License',
	description='',
	long_description=README,
	include_package_data=True,
	packages=find_packages(),
	install_requires=["django-extensions",
			"pygraphviz",
			"pyparsing",
			"pydot"],
			 #--install-option='--include-path=/usr/include/graphviz' --install-option='--library-path=/usr/lib/graphviz/'

	author='Manuel Machacón Cantillo',
	author_email='machaconmanuel@gmail.com',
	
	classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: Free To Use But Restricted',  # example license
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

	keywords='sample setuptools development django-extensions, database, db-graphviz, sql, orm, pydot',


	
)