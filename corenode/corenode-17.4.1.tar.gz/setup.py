from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'corenode',
  packages = find_packages(exclude=['config']),
  version = '17.04.01',
  description = 'CoreCluster node configuration and management package',
  author = 'Marta Nabozny',
  author_email = 'martastrzet@gmail.com',
  url = 'http://cloudover.org/corecluster/',
  download_url = 'https://github.com/cloudOver/CoreNode/archive/master.zip',
  keywords = ['corecluster', 'cloudover', 'cloud'],
  classifiers = [],
  install_requires = ['corenetwork'],
)
