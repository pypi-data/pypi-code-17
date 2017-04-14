from distutils.core import setup
from setuptools import find_packages
from distutils.command.install import install as _install


setup(
  name = 'coretalk',
  packages = find_packages(exclude=['config']),
  version = '17.04.01',
  description = 'CloudInit support for CoreCluster IaaS',
  author = 'Marta and Maciej Nabozny',
  author_email = 'marta.nabozny@gmail.com',
  url = 'http://cloudover.org/coretalk/',
  download_url = 'https://github.com/cloudOver/CoreTalk/archive/master.zip',
  keywords = ['corecluster', 'cloudover', 'cloud', 'cloudinit'],
  classifiers = [],
  install_requires = ['corecluster', 'pyaml'],
)
