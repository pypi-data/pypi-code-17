#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst').read()

# Pull in the package info
package_name = 'brothon'
package = __import__(package_name)
version = package.__version__
author = package.__author__
email = package.__email__

# Data and Example Files
def additional_files():
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cur_dir, 'data')
    for (dirpath, dirnames, files) in os.walk(data_path):
        for f in files:
            yield os.path.join(dirpath.split('/', 1)[1], f)
    example_path = os.path.join(cur_dir, 'examples')
    for (dirpath, dirnames, files) in os.walk(data_path):
        for f in files:
            yield os.path.join(dirpath.split('/', 1)[1], f)

setup(
    name=package_name,
    version=version,
    description='Bro + Python = Brothon!',
    long_description=readme,
    author=author,
    author_email=email,
    url='https://github.com/kitware/BroThon',
    packages=find_packages(),
    include_package_data=True,
    # data_files=['', [f for f in additional_files()]],
    install_requires=[
        'watchdog'
    ],
    license='Apache',
    zip_safe=False,
    keywords='Bro IDS, Python, Networking, Security',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
