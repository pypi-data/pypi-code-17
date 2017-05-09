# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='everyclient',
    version='0.1.2',
    description='Everysense client package for Rest API',
    long_description=readme,
    author='Everysense Inc',
    author_email='support@every-sense.com',
    url='https://github.com/every-sense',
    license='MIT',
    packages=find_packages(exclude=('tests', 'example', 'docs'))
)
