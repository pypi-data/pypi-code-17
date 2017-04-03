#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright 2011-2017 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from setuptools import setup


setup(
    name='django-pgtools',
    version='0.4',
    description="Set of Django management commands for handling various aspects of managing PostgreSQL database.",
    url='https://launchpad.net/django-pgtools',
    author='Canonical ISD',
    author_email='canonical-isd@lists.launchpad.net',
    packages=['pgtools', 'pgtools/management', 'pgtools/management/commands'],
    license='AGPLv3',
    requires=['django (>=1.6)']
)
