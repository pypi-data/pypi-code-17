try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESCRIPTION = """
This module implements cuckoo optimization algorithm introduced by Ramin Rajabioun
"""

setup(name='coa',
      version='0.1',
      description='Cuckoo Optimization Algorithm in Python',
      license='LGPLv3',
      author='Alireza Afzal aghaei',
      author_email='alirezaafzalaghaei@gmail.com',
      url='https://github.com/alirezaafzalaghaei/coa',
      long_description=LONG_DESCRIPTION,
      packages=['coa'],
      install_requires=['numpy', 'scipy'],
)
