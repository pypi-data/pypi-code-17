from distutils.core import setup
from setuptools import find_packages
setup(name='ml_buff',
        version='0.01',
        packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        author='Bruno Tinen',
        author_email='bruno.tinen@usp.br',
        license='MIT',
        )
