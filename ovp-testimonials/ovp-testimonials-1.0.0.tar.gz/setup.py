# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ovp-testimonials',
    version='1.0.0',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=find_packages(),
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-testimonials',
    download_url='https://github.com/OpenVolunteeringPlatform/django-ovp-testimonials/tarball/1.0.0',
    license='AGPL',
    description='This module has user testimonials functionality',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.5.3,<3.6.0',
      'codecov>=2.0.5,<2.1.0',
      'coverage>=4.2,<4.4.0',
      'ovp-users>=1.1.7,<2.0.0',
      'ovp-core>=1.2.4,<2.0.0',
      'ovp-uploads==1.0.3,<2.0.0',
      'djangorestframework-jwt>=1.9.0,<2.0.0',
      'whoosh>=2.7.4,<2.8.0',
    ]
)
