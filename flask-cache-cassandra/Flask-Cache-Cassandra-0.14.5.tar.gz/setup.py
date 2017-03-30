#!/usr/bin/env python
"""
Flask-Cache-Cassandra
-----------

Adds cache support to your Flask application

Includes a backend for 'cassandra'
"""

from setuptools import setup

setup(
    name='Flask-Cache-Cassandra',
    version='0.14.5',
    url='http://github.com/a-tal/flask-cache-cassandra',
    license='BSD',
    author='Thadeus Burgess',
    author_email='thadeusb@thadeusb.com',
    maintainer='Adam Talsma',
    maintainer_email='adam@talsma.ca',
    description='Adds cache support to your Flask application',
    long_description=__doc__,
    packages=['flask_cache'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask'],
    provides=['flask_cache'],
    obsoletes=['flask_cache'],
    test_suite='test_cache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
