#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "m_lib.defenc",
    version = "1.0.0",
    description = "Get default encoding",
    long_description = "Get default encoding. A part of Broytman Library for Python, Copyright (C) 1996-2017 PhiloSoft Design",
    author = "Oleg Broytman",
    author_email = "phd@phdru.name",
    url = "http://phdru.name/Software/Python/#m_lib",
    license = "GPL",
    keywords=[''],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms = "All",
    packages = ["m_lib"],
    namespace_packages = ["m_lib"],
)
