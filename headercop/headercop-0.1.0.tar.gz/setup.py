#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BSD License
#
# Copyright (c) 2017, Kaffi LLC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.


from setuptools import setup
try:
    import pypandoc
    HAVE_PYPANDOC = True
except ImportError:
    HAVE_PYPANDOC = False

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

long_description = readme + '\n\n' + changelog
if HAVE_PYPANDOC:
    long_description = pypandoc.convert_text(long_description, 'rst', format='md')

requirements = [
    'Click>=6.0',
    'PyYAML',
    'pathspec',
]

dev_requirements = [
    'ipdb',
    'ipython',
    'pip-tools',
    'pypandoc',  # Because pypi only takes rst style READMEs...
]

test_requirements = [
    'flake8',
    'pytest',
    'pytest-cov',
    'tox',
]

setup(
    name='headercop',
    version='0.1.0',
    description="Enforce license headers in files",
    long_description=long_description,
    author="Kaffi LLC",
    author_email='paul.collins@kaffi.io',
    url='https://gitlab.com/kaffi/headercop',
    packages=[
        'headercop',
    ],
    package_dir={'headercop':
                 'headercop'},
    entry_points={
        'console_scripts': [
            'headercop=headercop.cli:cmd'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements + test_requirements,
    },
    license="BSD license",
    zip_safe=False,
    keywords='headercop',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
