#!/usr/bin/env python
"""Setup Tools Script"""
import os
import codecs
from setuptools import setup, find_packages


PACKAGENAME = 'sqre-gtf'
DESCRIPTION = 'GitHub Protection, TravisCI and Flake8 tools for LSST DM.'
AUTHOR = 'J. Matt Peterson'
AUTHOR_EMAIL = 'jmatt@jmatt.org'
URL = 'https://github.com/lsst-sqre/gtf'
VERSION = '0.1.7'
LICENSE = 'MIT'


def read(filename):
    """Convenience function for includes"""
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return codecs.open(full_filename, 'r', 'utf-8').read()


long_description = read('README.md')  # pylint:disable=invalid-name


setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='lsst',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'sqre-github3.py==1.0.0a4',
        'GitPython==1.0.1',
        'MapGitConfig==1.1',
        'sqre-pytravisci==0.0.3',
        'sqre-codekit==2.1.0'
    ],
    tests_require=[
        'pytest==3.0.7',
        'pytest-cov==2.4.0',
        'pytest-flake8==0.8.1'],
    # package_data={},
    entry_points={
        'console_scripts': [
            'github-update = gtf.cli.update:main',
            'github-protect = gtf.cli.protect:main',
            'github-travis = gtf.cli.travis:main',
            'github-protect-travis = gtf.cli.github_protect_travis:main'
        ]
    }
)
