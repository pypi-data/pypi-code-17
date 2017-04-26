#!/usr/bin/env python3
# *-* coding: utf-8 *-*

from os import path
from setuptools import setup, find_packages

with open(path.join('crx_unpack', 'VERSION')) as v_file:
    version = v_file.read().strip()


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='crx_unpack',
    packages=find_packages(exclude=['docs', ]),
    package_data={'crx_unpack': ['VERSION']},
    scripts=['unpack'],
    version=version,
    license='MIT',
    description='Unpack .crx files the way Chrome does',
    long_description=read('README.rst'),
    author='Mike Mabey',
    author_email='mmabey@ieee.org',
    url='http://crx-unpack.readthedocs.io/',
    download_url='https://bitbucket.org/mmabey/crx_unpack/get/{}.tar.gz'.format(version),
    install_requires=[x.strip() for x in open(path.join(path.dirname(__file__), 'requirements.txt'))],
    keywords=[
        'crx',
        'unpack',
        'Chrome',
        'Chrome OS',
        'extension',
        'package',
    ],
    classifiers=[  # Full list at: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        # Operating systems supported
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        # Versions of Python supported
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
