#!/usr/bin/python
"""
The MIT License (MIT)

Copyright (c) 2017 Frantisek Lachman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function

import os
import pkgutil
import re
from distutils.version import StrictVersion

from setuptools import find_packages, setup

description = """Alternative image builder for docker containers.
Provides python2/python3 api and cli tool `incubator`.

Extends the functionality of basic `docker build` with precise layering,
ability to have build time volumes and some other useful options,
that can be given as a python dictionary or json file.
"""


def _get_version():
    _dirname = os.path.dirname(os.path.abspath(__file__))
    _version_file = open(os.path.join(_dirname, 'VERSION'))
    return _version_file.read().strip()


def _get_requirements(path):
    try:
        with open(path) as f:
            packages = f.read().splitlines()
    except (IOError, OSError) as ex:
        raise RuntimeError("Can't open file with requirements: %s", repr(ex))
    return [p.strip() for p in packages if not re.match(r"^\s*#", p)]


def _requires():
    return [r.replace('-', '_').split(">")[0] for r in _install_requirements()]


def _test_module(mod):
    return pkgutil.find_loader(mod) is not None


def _install_requirements():
    requirements = _get_requirements('requirements.txt')

    if _test_module("docker"):
        import docker
        is_old_api = StrictVersion(docker.__version__) < StrictVersion('2.0.0')
        if is_old_api:
            requirements.remove("docker")
            requirements.append("docker-py")
    return requirements


setup(
    name='incubator',
    version=_get_version(),
    description='Python library for building container images.',
    long_description=description,
    author='Frantisek Lachman',
    author_email='lachmanfrantisek@gmail.com',
    url='https://gitlab.com/lachmanfrantisek/incubator',
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=_install_requirements(),
    requires=_requires(),
    tests_require=_get_requirements('tests/requirements.txt'),
    entry_points='''
       [console_scripts]
       incubator=incubator.cli.incubator:cli
   ''',
    keywords='containers, build, docker, images',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Topic :: Software Development :: Build Tools',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: System :: Software Distribution',
                 ]
)
