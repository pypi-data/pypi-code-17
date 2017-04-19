# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='poslat',
    author='kusegorplay',
    version='1.0.0',
    packages=find_packages(),
    long_description="Пошли весело! :p",
    entry_points={
        'console_scripts': [
        'iditi = poslyat.poslat:_poslat'
        ]
    },
    install_requires=[
    'colorama==0.3.7'
]
)