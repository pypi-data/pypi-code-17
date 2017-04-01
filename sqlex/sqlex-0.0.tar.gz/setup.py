"""
setup packaging script for sqlex
"""

import os

version = "0.0"
dependencies = []

# allow use of setuptools/distribute or distutils
kw = {}
try:
    from setuptools import setup
    kw['entry_points'] = """
      [console_scripts]
      sqlex = sqlex.main:main
"""
    kw['install_requires'] = dependencies
except ImportError:
    from distutils.core import setup
    kw['requires'] = dependencies

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = open(os.path.join(here, 'README.txt')).read()
except IOError:
    description = ''


setup(name='sqlex',
      version=version,
      description="sql(ite) explorer/exporter",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/sqlex',
      license='',
      packages=['sqlex'],
      include_package_data=True,
      tests_require=['tox'],
      zip_safe=False,
      **kw
      )
