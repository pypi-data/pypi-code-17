from os import path
from setuptools import setup, find_packages


VERSION = '0.0.5'

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='reloadable',
    version=VERSION,
    description='Rerun a function upon failure',
    long_description=long_description,
    author='Diogo Magalhães Martins',
    author_email='magalhaesmartins@icloud.com',
    url='https://bitbucket.org/sievetech/reloadable',
    keywords='reloadable recover loop cli sieve',
    packages=find_packages(exclude=['tests']),
)
