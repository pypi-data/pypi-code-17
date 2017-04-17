#!/usr/bin/env python

from setuptools import setup
import os


def get_locals(filename):
    l = {}
    exec(open(filename, 'r').read(), {}, l)
    return l


metadata = get_locals(os.path.join('condor_csv', '_metadata.py'))

setup(
    name='condor_csv',

    version=metadata['__version__'],

    description='Make HTCondor submit files from CSV files',
    long_description='',

    # The project's main homepage.
    url='https://github.com/njvack/condor_csv',

    # Author details
    author=metadata['__author__'],
    author_email=metadata['__author_email__'],

    # Choose your license
    license=metadata['__license__'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords=' '.join([
        'parallel_computing',
        'high_throughput_computing',
        'science',
        'condor',
        'htcondor',
        'cluster'
    ]),

    tests_require=['pytest'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['condor_csv'],

    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'csv_to_submit=condor_csv.csv_to_submit:main',
        ],
    },
)
