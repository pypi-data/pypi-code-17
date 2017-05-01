#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Installer script for dockerscript
"""

import sys
from setuptools import find_packages, setup

__version__ = '0.8.0'

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

def read_requirements(filename: str):
    """
    Reads requirements from the given file
    """

    requirements = []
    dep_links = []

    with open(filename) as file_handle:
        for line in file_handle.readlines():
            line = line.strip()

            if line.startswith('git+https'):
                url, info = line.split('#')

                dep_links.append(url)
                requirements.append(info.split('=')[1])
            else:
                requirements.append(line)

    return requirements, dep_links

REQUIREMENTS, REQUIREMENTS_LINKS = read_requirements('requirements.txt')
TEST_REQUIREMENTS, TEST_REQUIREMENTS_LINKS = read_requirements('requirements_test.txt')

try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name='dockerscript',
    version=__version__,
    description='Tool for generating Dockerfiles from Python',
    long_description=README + '\n\n' + HISTORY,
    author='James Durand',
    author_email='james.durand@alumni.msoe.edu',
    url='https://github.com/durandj/dockerscript',
    packages=find_packages(exclude=['tests.*']),
    package_dir={
        'dockerscript': 'dockerscript',
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    dependency_links=REQUIREMENTS_LINKS + TEST_REQUIREMENTS_LINKS,
    license='MIT license',
    zip_safe=False,
    keywords='dockerscript',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
)
