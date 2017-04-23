#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pandas',
    'numpy',
    'bokeh'
]

test_requirements = [
    'pytest'
] + requirements

setup(
    name='tssim',
    version='0.1.1',
    description=".",
    long_description=readme + '\n\n' + history,
    author="Franz Woellert",
    author_email='franz.woellert@gmail.com',
    url='https://github.com/mansenfranzen/tssim',
    packages=[
        'tssim',
    ],
    package_dir={'tssim':
                 'tssim'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tssim',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest}
)
