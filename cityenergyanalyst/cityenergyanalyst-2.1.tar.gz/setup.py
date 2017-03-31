"""Installation script for the City Energy Analyst"""

import os
from setuptools import setup, find_packages

import cea

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = cea.__version__
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

if os.environ.get('READTHEDOCS', False) == 'True':
    # trick to make cea installable for readthedocs
    INSTALL_REQUIRES = ['geopandas', 'pandas', 'shapely', 'fiona', 'descartes', 'pyproj', 'xlrd', 'requests',
                        'doit==0.29.0', 'pyshp', 'pysal', 'ephem']
else:
    # TODO: list all the requirements for installing
    INSTALL_REQUIRES = ['geopandas', 'pandas', 'shapely', 'fiona', 'descartes', 'pyproj', 'xlrd', 'requests',
                        'doit==0.29.0', 'pyshp', 'pysal', 'ephem']


setup(name='cityenergyanalyst',
      version=__version__,
      description='City Energy Analyst',
      license='MIT',
      author='Architecture and Building Systems',
      author_email='cea@arch.ethz.ch',
      url='http://cityenergyanalyst.com',
      long_description=LONG_DESCRIPTION,
      py_modules=[''],
      packages=find_packages(),
      package_data={},
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      entry_points={
          'console_scripts': ['cea=cea.cli:main'],
      },
      )
