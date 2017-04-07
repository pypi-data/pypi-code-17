#!/usr/bin/env python
from distutils.core import setup, Extension

readme_conts = open("README.rst", "U").read()

procname_ext = Extension("procname", ["procnamemodule.c"])
setup(
    name="procname-redux",
    version="0.3",
    url="http://github.com/lericson/procname/",
    author="Eugene Pankov & Ludvig Ericson",
    author_email="e.pankov@syslink.de",
    description="Set process titles in Python programs",
    long_description=readme_conts,
    ext_modules=[procname_ext]
)
