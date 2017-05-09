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
"""Setup for zope.app.folder package

"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

version = '4.0.0'

tests_require = [
    'zope.app.container',
    'zope.browsermenu',
    'zope.browserpage',
    'zope.browserresource',
    'zope.configuration',
    'zope.testing',
    'zope.testrunner',
]

setup(name='zope.app.folder',
      version=version,
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Folder Content Type for Zope 3',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
          ),
      keywords="zope3 folder site local component",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://github.com/zopefoundation/zope.app.folder',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      install_requires=[
          'setuptools',
          'zope.container',
          'zope.site',
          'zope.app.content >= 4.0.0',
      ],
      extras_require={
          'test': tests_require,
          'zcml': [
              'zope.app.container',
              'zope.browsermenu',
              'zope.browserpage',
              'zope.browserresource',
          ],
      },
      tests_require=tests_require,
      include_package_data=True,
      zip_safe=False,
)
