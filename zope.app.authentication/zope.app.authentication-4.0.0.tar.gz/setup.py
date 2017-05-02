##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.authentication package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

tests_require = [
    'zope.app.security >= 4.0',
    'zope.app.rotterdam >= 4.0',
    'zope.app.basicskin >= 4.0',
    'zope.app.form >= 5.0',
    'zope.app.wsgi',
    'zope.app.schema',

    'zope.formlib',
    'zope.login',
    'zope.principalannotation',
    'zope.publisher >= 4.3.1',
    'zope.publisher',
    'zope.securitypolicy',
    'zope.session',
    'zope.site',
    'zope.testbrowser >= 5.2',
    'zope.testing',
    'zope.testrunner'
]

setup(name='zope.app.authentication',
      version='4.0.0',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description=('Principals and groups management for '
                   'the pluggable authentication utility'),
      long_description=(
        read('README.rst')
        + '\n\n.. contents::\n\n' +
        read('src', 'zope', 'app', 'authentication', 'README.rst')
        + '\n\n' +
        read('src', 'zope', 'app', 'authentication', 'principalfolder.rst')
        + '\n\n' +
        read('src', 'zope', 'app', 'authentication', 'vocabulary.rst')
        + '\n\n' +
        read('CHANGES.rst')
        ),
      url='http://github.com/zopefoundation/zope.app.authentication',
      license='ZPL 2.1',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3',
      ],
      keywords='zope3 authentication pluggable principal group',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      extras_require={
          'test': tests_require,
      },
      namespace_packages=['zope', 'zope.app'],
      install_requires=[
          'setuptools',
          'zope.authentication',
          'zope.component',
          'zope.container',
          'zope.dublincore',
          'zope.event',
          'zope.exceptions',
          'zope.formlib >= 4.0.2',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.location',
          'zope.password >= 3.5.1',
          'zope.pluggableauth >= 2.2.0',
          'zope.schema',
          'zope.security',
          'zope.traversing',
          # Needed for browser code.
          'zope.app.container >= 4.0.0',
          'zope.app.component >= 4.0.0',
          ],
      include_package_data=True,
      zip_safe=False,
)
