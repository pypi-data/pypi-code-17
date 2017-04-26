#! /usr/bin/env python

try:
    from setuptools import setup
    is_setuptools = True
except ImportError:
    from distutils.core import setup
    is_setuptools = False

kw = {}
if is_setuptools:
    kw['extras_require'] = {
        'Metakit': ['Mk4py'],
        'ZODB': ['ZODB'],
        'mx': ['mx.DateTime', 'mx.Misc'],
        }

setup(name = "m_lib",
    version = "3.1.0",
    description = "Broytman Library for Python",
    long_description = "Broytman Library for Python, Copyright (C) 1996-2017 PhiloSoft Design",
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
    packages = ["m_lib", "m_lib.clock", "m_lib.flad",
        "m_lib.hash", "m_lib.lazy",
        "m_lib.net", "m_lib.net.ftp", "m_lib.net.www",
        "m_lib.pbar", "m_lib.rus",
    ],
    namespace_packages = ["m_lib"],
    **kw
)
