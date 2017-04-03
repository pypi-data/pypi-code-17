# coding: utf-8

import os
import re
import glob
from setuptools import setup


def find_version(*file_paths):
    with open(os.path.join(*file_paths)) as fhandler:
        version_file = fhandler.read()
        version_match = re.search(r"^__VERSION__ = ['\"]([^'\"]*)['\"]",
                                  version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="python-ctp-deps",
    packages=[
        "ctp_deps",
    ],
    data_files=[
        ("ctp_deps/include", glob.glob("ctp_deps/include/*.h")),
        ("ctp_deps/lib", glob.glob("ctp_deps/lib/*")),
        ("ctp_deps/misc", glob.glob("ctp_deps/misc/*")),
    ],
    version=find_version("ctp_deps", "__init__.py"),
    license="BSD License",
    description="Dynamic Shared Libraries (.so) for CTP",
    author="PAN, Myautsai",
    author_email="myautsai@gmail.com",
    url="https://github.com/mckelvin/python-ctp-deps",
    keywords=["ctp", "sfit"],
    long_description=open("README.rst").read(),
    include_package_data=True,
    zip_safe=False,
)
