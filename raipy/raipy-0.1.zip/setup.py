# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'GUI for measurements'

setup(
    name  = 'raipy',
    version = '0.1',
    description = 'GUI for measurements',
    long_description = long_description,
    license = 'MIT',
    author = 'Yuki Arai',
    author_email = 'threemeninaboat3247@gmail.com',
    url = 'https://github.com/threemeninaboat3247/raipy',
    keywords = 'GUI',
    packages = find_packages(),
    install_requires = ['pyqtgraph','numpy'],
    classifiers = [
      'Programming Language :: Python :: 3.5',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License'
    ]
)
