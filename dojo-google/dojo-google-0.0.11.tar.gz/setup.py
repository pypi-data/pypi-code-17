#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo-google',
    version='0.0.11',
    description='Dojo transforms using Google APIs.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_google', ],
    install_requires=[
        'dojo',
        'google-api-python-client',
        'google-cloud-dataflow',
        'retrying'
    ]
)
