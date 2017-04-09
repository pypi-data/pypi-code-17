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

import pkgutil
import re
from distutils.version import StrictVersion

from setuptools import find_packages, setup


def _get_version():
    version_file = open('VERSION')
    version = version_file.read().strip()
    return version


def _get_requirements(path):
    try:
        with open(path) as f:
            packages = f.read().splitlines()
    except (IOError, OSError) as ex:
        raise RuntimeError("Can't open file with requirements: %s", repr(ex))
    return [p.strip() for p in packages if not re.match(r"^\s*#", p)]


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
            # print("Already have docker api. Using old API.")
        else:
            # print("Already have docker api. Using new API.")
            pass
    for r in requirements:
        print(r)
    return requirements


setup(
    name='incubator',
    version=_get_version(),
    description='Python library for building container images.',
    author='Frantisek Lachman',
    author_email='lachmanfrantisek@gmail.com',
    url='https://gitlab.com/lachmanfrantisek/incubator',
    license="MIT",
    test_suite="tests",
    packages=find_packages(exclude=["tests"]),
    install_requires=_install_requirements(),
    tests_require=_get_requirements('tests/requirements.txt'),
    entry_points='''
       [console_scripts]
       incubator=incubator.cli.incubator:cli
   ''',
)
