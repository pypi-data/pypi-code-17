"""Setup script for jwxml (based on the PyPA guide)

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

root = path.abspath(path.dirname(__file__))
NAME = 'jwxml'

# Get the long description from the README file
with open(path.join(root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(root, NAME, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name=NAME,

    # Versions should comply with PEP440.
    version=version,

    description='Parse and manipulate XML files, mostly JWST optics and wavefront sensing related.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mperrin/jwxml',

    # Author details
    author='Marshall Perrin, Joseph Long',
    author_email='help@stsci.edu',
    license='BSD',
    keywords='jwst xml siaf',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # OS support
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],


    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['numpy>=1.9', 'matplotlib>=1.4.3'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest>=0.34', 'lxml>=3.6.4', 'pytest>=3.0.2'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'jwxml': [
            'VERSION',
            'data/*/*.xml'
        ],
    },
)