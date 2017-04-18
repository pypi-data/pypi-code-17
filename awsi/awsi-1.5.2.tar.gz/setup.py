#!/usr/bin/env python
import sys, os, setuptools

PACKAGE_NAME = 'awsi'
MINIMUM_PYTHON_VERSION = 2, 7

def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


def read_descriptions():
    """Build a description for the project from documentation files."""
    try:
        readme = open("README.md").read()
    except IOError:
        return "<placeholder>"
    else:
        return readme + '\n'


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert 0, "'{0}' not found in '{1}'".format(key, module_path)
    

check_python_version()
setuptools.setup(
    name=read_package_variable('__project__'),
    version=read_package_variable('__version__'),
    description='AWS EC2 information and connection tool',
    long_description=read_descriptions(),
    url='http://gitlab.com/cuotos/awsi',
    author='Dan Potepa',
    author_email='dan@danpotepa.co.uk',
    license='wtfpl',
    packages=['awsi'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    install_requires=[
    	'boto==2.45.0'
    ],
    entry_points = {
        'console_scripts': ['awsi=awsi.awsi:main'],
    },
    zip_safe=False
)
