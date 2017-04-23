#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

# (C) 2017, Eike Jesinghaus
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from setuptools import setup

try:
    from bdist_nsi import bdist_nsi
except:
    pass

setup(
    name='Nano-Assault',
    version='1.0',
    url="https://edugit.org/eike/nanoassault",
    author="Eike Jesinghaus",
    author_email="eike@naturalnet.de",
    packages=['nanoassault'],
    package_data={
                  'nanoassault': ["img/*.png", "sound/*.wav"],
                 },
    zip_safe=False,
    install_requires=[
                      'Pygame',
                     ],
    entry_points={
                  'gui_scripts': [
                                  'nanoassault = nanoassault:main',
                                 ],
                 },
    classifiers=[
                 "Development Status :: 6 - Mature",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Topic :: Games/Entertainment :: Arcade"
                ],
    options={"bdist_nsi": {}}
)
