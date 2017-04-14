from distutils.core import setup
from setuptools import find_packages
from distutils.command.install import install as _install

import subprocess
import shutil
import os

setup(
  name = 'corenetwork',
  packages = find_packages(exclude=['config']),
  version = '17.04.01',
  description = 'CoreCluster common networking package',
  author = 'Marta Nabozny',
  author_email = 'martastrzet@gmail.com',
  url = 'http://cloudover.org/corecluster/',
  download_url = 'https://github.com/cloudOver/CoreCluster/archive/master.zip',
  keywords = ['corecluster', 'corenetwork', 'cloudover', 'cloud'],
  classifiers = [],
  install_requires = ['django', 'requests', 'simplejson', 'netifaces', 'netaddr'],
)
