#!/usr/bin/env python
# coding: utf8

# Copyright 2017 Vincent Jacques <vincent@vincent-jacques.net>

import setuptools

version = "0.1.0"


setuptools.setup(
    name="devlpr",
    version=version,
    description="Library to help software developers with their recurrent tasks",
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://pythonhosted.org/devlpr/",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
    ],
    install_requires=[],
    tests_require=[],
    test_suite="devlpr.tests",
    use_2to3=True,
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    },
)
