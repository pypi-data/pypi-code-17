"""A setuptools based setup module.
See: https://packaging.python.org/en/latest/distributing.html
     https://github.com/pypa/sampleproject
"""

import os
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

version = '0.4.0'

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ObjDict',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='The ObjDict class has many uses including: as a tool for processing and '
                'generating json information, for ad-hoc classes and mutable named tuples, '
                'or just as dictionaries that allow dot notation access.',

    # Contents of the README file
    long_description=long_description,

    # The project's main homepage.
    url='https://bitbucket.org/objdict/objdict',

    # Author details
    author='Ian Ogilvy',
    author_email='ian.ogilvy@saltmobile.com',

    # Choose your license
    license='LGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',

        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='object dictionary tuples namedtuples namedlists JSON custom classes',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['build', 'contrib', 'dist', 'docs', 'tests']),

    include_package_data=True,
    zip_safe=False,

    install_requires=[
        # -*- Extra requirements: -*-
    ],

    entry_points="""
    # -*- Entry points: -*-
    """
)
