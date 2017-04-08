# -*- coding: utf-8 -*-

import os
from setuptools import setup


setup(
    name="gsub",
    description="Replacement for git-submodule",

    version="0.1.2",

    author="Amit Upadhyay",
    author_email="code@amitu.com",

    url="https://github.com/Coverfox/gsub",
    license="BSD",


    install_requires=["click==6.6"],

    packages=['gsub'],
    zip_safe=True,


    keywords=['git', 'git submodule'],


    classifiers=[

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'Natural Language :: English',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',

        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development',

    ],
    entry_points={
        'console_scripts': [
            'gsub = gsub.main:main',
        ],
    },
)
