#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "sectorizedradialprofile",
    version = "1.0.0",
    author = "Jean Bilheux",
    author_email = "bilheuxjm@ornl.gov", 
    packages = find_packages(exclude=['tests', 'notebooks']),
    include_package_data = True,
    test_suite = 'tests',
    install_requires = [
        'numpy',
        'pyfits',
        'pillow',
    ],
    dependency_links = [
    ],
    description = "Radial profile of a given sector of an 2D array",
    license = 'BSD',
    keywords = "tiff tif profile radial sector",
    url = "https://github.com/JeanBilheux/SectorizedRadialProfile",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'],
)


# End of file
