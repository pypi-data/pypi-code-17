from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

PACKAGE1_NAME = "shruutils"
VERSION = "1.0.0"

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE1_NAME,
    version=VERSION,

    description='A sample Python project',
    long_description=long_description,

    packages=["utils"],

    install_requires=['peppercorn'],


)