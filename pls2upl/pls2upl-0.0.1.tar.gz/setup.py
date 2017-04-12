#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pls2upl import __version__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "click~=6.7",
    "mutagen~=1.37",
]

test_requirements = [
]

setup(
    name='pls2upl',
    version=__version__,
    description="pls2upl is a command-line utility for converting PLS/M3U playlists to UPL",
    long_description=readme,
    author="Stavros Korokithakis",
    author_email='hi@stavros.io',
    url='https://gitlab.com/universal-playlist/pls2upl/',
    packages=[
        'pls2upl',
    ],
    package_dir={'pls2upl':
                 'pls2upl'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords="music universal playlist pls m3u upl",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'pls2upl=pls2upl.cli:cli',
        ],
    },
)
