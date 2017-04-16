# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from accessor import __version__

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Framework :: Django',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License'
]

REQUIREMENTS = []

setup(
    name='accessor',
    version=__version__,
    description='A simple python module for resolving paths on python objects',
    long_description=open('README.rst').read(),
    author='Veit Rückert',
    author_email='veit.rueckert@web.de',
    url='http://github.com/schwobaseggl/accessor',
    download_url='http://github.com/schwobaseggl/accessor/archive/{}.tar.gz'.format(__version__),
    packages=['accessor'],
    keywords="accessor attribute key index resolve",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
)
