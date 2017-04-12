#!/usr/bin/env python
from setuptools import setup

setup(
    name='jio',
    version='0.0.2',
    description="Jacobi's basic IO functions and helpers",
    author='Jacobi Petrucciani',
    author_email='jacobi@mimirhq.com',
    url='https://jacobi.gitly.io/jio',
    license='MIT',
    packages=['jio'],
    test_suite='nose.collector',
    tests_require=['nose']
)
