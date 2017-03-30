#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'martinellis'
    ,version = '1.0.0'
    ,author = 'frank2'
    ,author_email = 'frank2@dc949.org'
    ,description = 'A python library for manipulating IPv4 and IPv6 addresses.'
    ,license = 'GPLv3'
    ,keywords = 'cidr ip ipv4 ipv6'
    ,url = 'https://github.com/frank2/martinellis'
    ,package_dir = {'martinellis': 'lib'}
    ,packages = ['martinellis']
    ,long_description = '''Martinellis-- named after the famous brand of cider-- is a library for manipulating
IP addresses in various formats. It allows for arbitrary masking of addresses and can
perform tasks such as randomization of a large ranges of addresses.'''
    ,classifiers = [
        'Development Status :: 5 - Production/Stable'
        ,'Topic :: Internet'
        ,'Topic :: Software Development :: Libraries'
        ,'License :: OSI Approved :: GNU General Public License v3 (GPLv3)']
)
