import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'zc', 'configuration', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        )

setup(
    name = "zc.configuration",
    version='1.2.0',
    description = "Extensions to zope.configuration",
    long_description = long_description,
    license = "ZPL 1.1",
    packages = find_packages('src'),
    include_package_data = True,
    zip_safe = False,
    package_dir = {'':'src'},
    namespace_packages = ['zc'],
    install_requires = [
        'setuptools',
        'zope.testing',
        'zope.configuration>=3.5.0',
        ],
    )
