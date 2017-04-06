#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

setup(
    name='pytest-selenium-pdiff',
    version='0.4.0',
    description="A pytest package implementing perceptualdiff for Selenium tests.",
    long_description=readme + '\n\n' + history,
    author="Phil Plante",
    author_email='phil@rentlytics.com',
    url='https://github.com/rentlytics/pytest-selenium-pdiff',
    packages=[
        'pytest_selenium_pdiff',
    ],
    entry_points={
        'pytest11': [
            'selenium_pdiff = pytest_selenium_pdiff.pytest_selenium_pdiff',
        ]
    },
    include_package_data=True,
    install_requires=[
        'pytest>=2.9.2',
        'pytest-selenium>=1.3.1',
        # used to call perceptualdiff util
        'sh==1.11',
        'pillow==4.0.0',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    test_suite='tests',
    tests_require=[
        'pytest==3.0.7',
        'pytest-cov',
        'pytest-html',
        'mock',
    ],
    license="MIT",
    zip_safe=False,
    keywords='pytest selenium pdiff perceptualdiff',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Framework :: Pytest",
    ]
)
