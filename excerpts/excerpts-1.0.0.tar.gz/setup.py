# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='excerpts',
    version='1.0.0',
    description='Excerpt Markdown Style Comments From a File',
    long_description=long_description,
    author='Andreas Dominik Cullmann',
    author_email='fvafrcu@arcor.de',
    url='https://github.com/fvafrcu/excerpts',
    license='BSD',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Documentation',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    keywords='table of contents, structure comments', 
    extras_require={
        'test': ['coverage'],
    },
    packages=find_packages(exclude=('tests', 'docs', 'output', 'utils', 
                                    'codes_doxygen')),
    entry_points = {
        'console_scripts': ['excerpts=excerpts.command_line:main'],
        }
)

