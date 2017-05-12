#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='dojo-google',
    version='0.0.16',
    description='Dojo transforms using Google APIs.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    install_requires=[
        'dojo',
        'google-api-python-client',
        'google-cloud-dataflow',
        'retrying'
    ]
)
