# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
# Copyright © 2009–2011 Canonical Ltd.
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

import os.path
import textwrap

from setuptools import (
    find_packages,
    setup,
)

import configdeck


install_requires = ['pyxdg']


main_module_name = 'configdeck'
main_module_fromlist = ['_metadata']
main_module = __import__(
        main_module_name,
        level=0, fromlist=main_module_fromlist)
metadata = main_module._metadata

version_file_path = os.path.join(os.path.dirname(__file__), "VERSION")
version_text = metadata.get_version_text(version_file_path)


setup(
    name='configdeck',
    version=version_text,
    description="Stacked configuration sources for your application.",
    long_description=textwrap.dedent("""\
        configdeck is a library that stacks together Python's
        optparse.OptionParser and ConfigParser.ConfigParser, so that
        you don't have to repeat yourself when you want to export the
        same options to a configuration file and a commandline
        interface.
        """),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        (
            'License :: OSI Approved'
            ' :: GNU General Public License v3 or later (GPLv3+)'),
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        ],
    maintainer='Ben Finney',
    maintainer_email='ben+python@benfinney.id.au',
    url='https://pagure.io/python-configdeck',
    license='GNU GPL v3 or later',
    install_requires=install_requires,
    dependency_links=['http://www.freedesktop.org/wiki/Software/pyxdg'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        main_module_name: ['VERSION'],
        },
    zip_safe=True,
    test_suite='configdeck.tests',
    tests_require=[
        'mock',
        'coverage',
        ],
    )
