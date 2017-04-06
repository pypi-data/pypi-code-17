#! /usr/bin/env python
# coding: utf-8

#  __author__ = 'ZhouHeng'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
from JYAliYun import pkg_info

if sys.version_info <= (2, 7):
    sys.stderr.write("ERROR: jingyun aliyun python sdk requires Python Version 2.7 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

setup(name=pkg_info.name,
      version=pkg_info.version,
      author=pkg_info.author,
      author_email="zhouheng@gene.ac",
      url=pkg_info.url,
      packages=["JYAliYun", "JYAliYun/AliYunMNS", "JYAliYun/Tools"],
      license=pkg_info.license,
      description=pkg_info.short_description,
      long_description=pkg_info.long_description,
      keywords=pkg_info.keywords
)