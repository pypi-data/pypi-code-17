# coding:utf-8

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 6):
    error = 'ERROR: anchcloud-sdk requires Python Version 2.7.'
    print >> sys.stderr, error
    sys.exit(1)

setup(
    name='anchcloud-sdk',
    version='0.0.1',
    description='Software Development Kit for AnchCloud.',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    keywords='anchcloud iaas qingstor sdk',
    author='chenyl',
    author_email='chenyl@51idc.com',
    url='',
    packages=['anchcloud', 'anchcloud.iaas', 'anchcloud.conn',
              'anchcloud.misc'],
    package_dir={'anchcloud-sdk': 'anchcloud'},
    namespace_packages=['anchcloud'],
    include_package_data=True,
    install_requires=['oauth2', 'datetime']
)
