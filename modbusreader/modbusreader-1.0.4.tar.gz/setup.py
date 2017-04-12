#!/usr/bin/env python3

import re
from setuptools import setup

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'


def get_version():
    with open('modbusreader/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""", version_file.read()).group('version')

install_requires = []

setup(
    name='modbusreader',
    packages=['modbusreader'],
    version=get_version(),
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
    package_data={
        "modbusreader": [
            "modbus_definition.schema.json",
        ],
    },
    include_package_data=True
)
