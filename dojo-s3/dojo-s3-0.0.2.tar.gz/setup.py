#!/usr/bin/env python

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dojo-s3',
    version='0.0.2',
    description='Dojo store, source, and sink adapters for AWS S3.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_s3', ],
    install_requires=requirements
)
