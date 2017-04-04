#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'pycountry>=16.10.23rc3',
]

setup(
    name='address-formatter',
    version='0.1.2',
    description="""Python module to parse and render postal addresses
        respecting country standard""",
    long_description=readme,
    author="Fulfil.IO Inc.",
    author_email='info@fulfil.io',
    url='https://github.com/fulfilio/address-formatter',
    packages=find_packages(),
    install_requires=requirements,
    license="BSD license",
    keywords='address-formatter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=[]
)
