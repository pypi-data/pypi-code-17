#!/usr/bin/env python
from setuptools import setup

setup(
    name='snappy-stream',
    version='0.9.0',
    url='https://github.com/CurataEng/snappy-stream',
    license='MIT',
    author='Scott Ivey / Curata Inc.',
    author_email='scott@curata.com',
    description='Streaming snappy compression for Python file-like objects, with helpers for local FS + S3',
    packages=['snappy_stream'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'python-snappy>=0.5',
        'six>=1.10.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)