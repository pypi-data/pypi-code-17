#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


def main():
    description = 'SQLAlchemy statement profiler for unit testing'

    setup(
        name='sqlalchemy-profile',
        version='0.1.0',
        description=description,
        long_description=description,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Intended Audience :: Developers',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'sqlalchemy',
        ],
        tests_require=[],
        setup_requires=[],
    )


if __name__ == '__main__':
    main()
