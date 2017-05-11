# -*- coding: utf-8 -*-
"""
This module contains the tool of birdhousebuilder.recipe.docker
"""
from setuptools import find_packages
from setuptools import setup

name = 'birdhousebuilder.recipe.docker'

version = '0.5.3'
description = 'A Buildout recipe to generate a Dockerfile for Birdhouse applications.'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

entry_points = '''
[zc.buildout]
default = %(name)s:Recipe
[zc.buildout.uninstall]
default = %(name)s:uninstall
''' % globals()

reqs = ['setuptools',
        'zc.buildout',
        'Mako', ]
tests_reqs = ['zc.buildout', 'zope.testing']

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
      keywords='buildout recipe birdhouse docker',
      author='Birdhouse',
      author_email="wps-dev at dkrz.de",
      url='https://github.com/bird-house/birdhousebuilder.recipe.docker',
      license='Apache License 2',
      install_requires=reqs,
      extras_require=dict(tests=tests_reqs),
      entry_points=entry_points,
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['birdhousebuilder', 'birdhousebuilder.recipe'],
      include_package_data=True,
      zip_safe=False, )
