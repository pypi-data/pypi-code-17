#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import versioneer

setup(
    name='lenastrips',
    author="doubleO8",
    author_email="wb008@hdm-stuttgart.de",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Controller for power strips as manufactered by ANEL Elektronik',
    long_description="",
    url="https://github.com/doubleO8/lenastrips",
    packages=['lenastrips'],
    scripts=['lena-strips-ctl.py']
)
