#!/usr/bin/env python3

# veripeditus-server - Server component for the Veripeditus game framework
# Copyright (C) 2016, 2017  Dominik George <nik@naturalnet.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version, with the Game Cartridge Exception.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from pkg_resources import get_distribution
from setuptools import setup

def requires_alternative(*alternatives):
    """ Allows specifying alternative requirements.

    This function takes arbitrarily many distribution specifications as arguments.
    It then checks for availability of each. If a distribution is found, the original
    specification for it is returned. If none of the alternatives is available,
    the first specified one is returned, causing setuptools to install it.
    """

    # Allow calling with both a list and several arguments
    if not isinstance(alternatives[0], str):
        alternatives = alternatives[0]

    # Iterate over all listed alternatives
    for alternative in alternatives:
        # Try to find a distribution with this specification
        try:
            get_distribution(alternative)
            # If we got here, return this specification as requirement,
            # it was the first we found
            return alternative
        except:
            # Not found, go on
            continue

    # If we got here, no alternative is installed yet, so return the first
    return alternatives[0]

# Dependency list
# Defined ahead of time so we can dynamically modify it later
DEPS = [
        requires_alternative('file-magic', 'magic'),
        'Flask>=0.10',
        'Flask-Restless>=1.0.0b2.dev0',
        'Flask-SQLAlchemy',
        'GitPython',
        'gpxpy',
        'OSMAlchemy>=0.1.4.dev0',
        'passlib',
        'setuptools',
        'Shapely',
        'SQLAlchemy>=1.1.0',
        'SQLAlchemy-Utils',
       ]

if os.environ.get('READTHEDOCS') == 'True':
    # Modify dependency list to enable build on RDT
    # RDT does not support C modules and Flask-Restless is unpublished
    DEPS.remove('Shapely')
    DEPS.remove('Flask-Restless>=1.0.0b2.dev0')
    DEPS.append('Flask-Restless>=1.0.0b1')

setup(
    name='Veripeditus',
    version='1.0.0a3',
    long_description = open(os.path.join(os.path.dirname(__file__), "README.rst"),
                            "r", encoding="utf-8").read(),
    url="http://www.veripeditus.org",
    author="The Veripeditus Team and contributors",
    author_email="team@veripeditus.org",
    packages=[
              'veripeditus.framework',
              'veripeditus.server',
              'veripeditus.editor',
              'veripeditus.game.test',
             ],
    namespace_packages=[
                        'veripeditus',
                        'veripeditus.game',
                       ],
    include_package_data=True,
    package_data={
                  'veripeditus.framework': ['data/*'],
                  'veripeditus.editor': ['data/*'],
                  'veripeditus.game.test': ['data/*'],
                 },
    zip_safe=False,
    install_requires=DEPS,
    dependency_links=[
                      "git+http://github.com/jfinkels/flask-restless#egg=Flask-Restless-1.0.0b2.dev0"
                     ],
    test_suite='test',
    entry_points={
                  'console_scripts': [
                                      'veripeditus-standalone = veripeditus.server:server_main',
                                      'veripeditus-newgame = veripeditus.editor.sdk:newgame_main'
                                     ]
                 },
    classifiers=[
                 "Development Status :: 3 - Alpha",
                 "Environment :: Web Environment",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Education",
                 "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Education",
                 "Topic :: Games/Entertainment",
                 "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
                 "Topic :: Software Development :: Libraries :: Application Frameworks",
                ],
)
