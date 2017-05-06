"""
Verktyg SQLAlchemy
==================

Utility library for connecting to databases from inside a verktyg application
using sqlalchemy
"""
from setuptools import setup, find_packages


setup(
    name='verktyg-sqlalchemy',
    version='0.3.0',
    url='https://github.com/bwhmather/verktyg-sqlalchemy',
    license='BSD',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    description='Library for using sqlalchemy in vertyg applications',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    install_requires=[
        'verktyg >= 0.9, < 0.10',
        'SQLAlchemy >= 1.1.9, < 2.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    test_suite='verktyg_sqlalchemy.tests.suite',
)
