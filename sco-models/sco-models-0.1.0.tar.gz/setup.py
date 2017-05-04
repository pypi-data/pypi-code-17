#! /usr/bin/env python

from setuptools import setup

setup(
    name='sco-models',
    version='0.1.0',
    description='Repository for registered models in the Standard Cortical Observer',
    keywords='neuroscience vision cortex ',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    url='https://github.com/heikomuller/sco-models',
    license='GPLv3',
    packages=['scomodels'],
    package_data={'': ['LICENSE']},
    install_requires=['sco-datastore']
)
