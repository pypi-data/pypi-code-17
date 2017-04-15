#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo-sentry',
    version='0.0.1',
    description='Dojo error handler for Sentry',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_sentry', ],
    install_requires=['dojo', 'raven']
)
