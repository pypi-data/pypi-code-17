#!/usr/bin/env python

from setuptools import setup

setup(
    name='do-client',
    version='1.0.6',
    description='DigitalOcean REST API python client',
    author='Sriram Velamur',
    author_email='sriram.velamur@gmail.com',
    url='https://github.com/techiev2/doclient',
    packages=['doclient',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=['requests','pyopenssl>=0.13','ndg-httpsclient','pyasn1']
)
