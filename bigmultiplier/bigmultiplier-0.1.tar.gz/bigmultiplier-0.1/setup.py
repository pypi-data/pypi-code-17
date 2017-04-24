#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from distutils.core import setup

import bigmultiplier

long_description = open('README.rst').read()

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='bigmultiplier',
    version=bigmultiplier.__version__,
    description='A package for help matrix multiplication',
    long_description=long_description,
    author=bigmultiplier.__author__,
    author_email='orcungumus@gmail.com',
    install_requires=reqs,
    url='https://github.com/somedanalytics/big-multiplier',  # use the URL to the github repo
    download_url='https://github.com/guemues//big-multiplier/archive/1.0.tar.gz'
)