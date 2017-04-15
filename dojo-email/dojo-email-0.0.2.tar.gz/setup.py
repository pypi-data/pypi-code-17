#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo-email',
    version='0.0.2',
    description='Dojo email drop source adapter',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_email', ],
    install_requires=['dojo', ]
)
