# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.

from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'cloud_ftp',
    packages = find_packages(),
    version = 'v1.0.1',
    description = 'Convenience wrapper for downloading FTP files on Google App Engine',
    author = 'Real Kinetic',
    author_email = 'dev@realkinetic.com',
    url = 'https://github.com/RealKinetic/cloud-ftp',
    download_url = 'https://github.com/RealKinetic/cloud-ftp/archive/v1.0.1.tar.gz',
    keywords = ['app engine', 'ftp'],
    classifiers = [],
)
