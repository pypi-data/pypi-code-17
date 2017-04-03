# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ovp-news',
    version='0.1.0',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/OpenVolunteeringPlatform/ovp-news',
    download_url = 'https://github.com/OpenVolunteeringPlatform/ovp-news/tarball/0.1.0',
    license='AGPL',
    description='This module contains  functionality for' + \
                ' sending newsletter and digests to users and leads',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.5.0,<3.6.0',
      'djangorestframework-jwt>=1.8.0,<2.0.0',
      'ovp-core>=1.2.4,<2.0.0',
      'ovp-users>=1.1.4,<2.0.0',
    ]
)
