#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo-jdbc',
    version='0.0.1',
    description='Dojo store, source, and sink adapters for JDBC connections with Apache Spark.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_jdbc', ],
    install_requires=['dojo', ]
)
