#!/usr/bin/env python

import setuptools
from glob import glob

setuptools.setup(
    name='ngless_cwl',
    packages=setuptools.find_packages(),
    version="0.0.1",
    description='ngless wrappers for common operations and use with CWL workflows',
    maintainer='NGLess team',
    maintainer_email='ngless@googlegroups.com',
    license='MIT',
    platforms=["any"],
    url="https://github.com/luispedro/NGLess",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    scripts=glob("bin/ngless-*.py"),
)
