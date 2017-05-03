# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Reggie team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Reggie the Registration and Management System"""

import os
from setuptools import setup, find_packages


# Package versioning solution originally found here:
# http://stackoverflow.com/q/458550
exec(open(os.path.join('reggie', '_version.py')).read())

reqs = open('requirements.txt', 'r').read().strip().splitlines()

setup(
    name='reggie',
    version=__version__,
    url='http://reggie.readthedocs.org',
    download_url='http://pypi.python.org/pypi/reggie',
    license='BSD',
    author='Rob Ruana',
    author_email='rob@robruana.com',
    description=__doc__,
    long_description=open('README.rst', 'r').read(),
    zip_safe=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Groupware',
        'Topic :: Office/Business :: Scheduling',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=reqs
)
