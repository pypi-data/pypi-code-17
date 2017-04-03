#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import modbusreader

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'


install_requires = []

setup(
    name='modbusreader',
    packages=['modbusreader'],
    version=modbusreader.__version__,
    license='MIT',
    description='Read values of a modbus server automatically based on a defined config',
    author='Stephan Müller',
    author_email='mail@stephanmueller.eu',
    url='https://github.com/smueller18/modbusreader',
    download_url='https://github.com/smueller18/modbusreader',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        "jsonschema",
        "pymodbus3"
    ],
    data_files=[
        ('config', ['config/modbus_definition.schema.json'])
    ]
)
