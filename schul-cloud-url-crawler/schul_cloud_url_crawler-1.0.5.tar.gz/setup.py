# coding: utf-8

"""
Schul-Cloud Url Crawler
"""


import sys
import os
from setuptools import setup, find_packages

NAME = "schul_cloud_url_crawler"
VERSION = "1.0"
if os.environ.get("TRAVIS_BUILD_NUMBER"):
    # same as in ../generate_python_client.sh
    VERSION += "." + os.environ.get("TRAVIS_BUILD_NUMBER")
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

HERE = os.path.dirname(__file__) or "."

REQUIRES = [line.strip() for line in open(os.path.join(HERE, "requirements.txt")).readlines() if line.strip()]

setup(
    name=NAME,
    version=VERSION,
    description="Crawler for Schul-Cloud Ressources",
    author_email="",
    url="https://github.com/schul-cloud/url-crawler",
    keywords=["Schul-Cloud Content API", "Crawler"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=open(os.path.join(HERE, "README.rst")).read()
)

