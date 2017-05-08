#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <ytjia.zju@gmail.com>

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()


def readme():
    with open('README.md') as f:
        return f.read()


def changelog():
    with open('CHANGELOG.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


settings.update(
        name='utils_py',
        version='0.2.0',
        description='Utility package for python',
        long_description=readme(),
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Utilities',
        ],
        keywords='python utility',
        url='https://github.com/ytjia/utils_py',
        author='Y. Jia',
        author_email='ytjia.zju@gmail.com',
        license='Apache 2.0',
        packages=['utils_py'],
        install_requires=requirements(),
        test_suite='nose.collector',
        tests_require=['nose'],
        include_package_data=True,
        zip_safe=False,
)

setup(**settings)
