# -*- coding: utf-8 -*-

#    `ionics` is a software which models various ionization cross sections.
#    Copyright (C) 2017  Dominik Vilsmeier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

"""
Material data for xenon.

References
----------
(1) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.445, TABLE I)
"""

shells = {  # Ref.(1)
    '1s': {
        'binding energy': 3456.4,
        'average kinetic energy': 38.8996e3,
        'occupation number': 2
    },
    '2s': {
        'binding energy': 5452.8,
        'average kinetic energy': 9240.0,
        'occupation number': 2
    },
    '2p': {
        'binding energy': 4889.4,
        'average kinetic energy': 8229.7,
        'occupation number': 6
    },
    '3s': {
        'binding energy': 1093.2,
        'average kinetic energy': 2481.8,
        'occupation number': 2
    },
    '3p': {
        'binding energy': 957.7,
        'average kinetic energy': 2412.9,
        'occupation number': 6
    },
    '3d': {
        'binding energy': 672.3,
        'average kinetic energy': 2283.8,
        'occupation number': 10},
    '4s': {
        'binding energy': 213.8,
        'average kinetic energy': 696.9,
        'occupation number': 2
    },
    '4p': {
        'binding energy': 146.7,
        'average kinetic energy': 635.3,
        'occupation number': 6
    },
    '4d': {
        'binding energy': 68.21,
        'average kinetic energy': 495.7,
        'occupation number': 10
    },
    '5s': {
        'binding energy': 23.3,
        'average kinetic energy': 110.4,
        'occupation number': 2
    },
    '5p': {
        'binding energy': 12.56,
        'average kinetic energy': 79.74,
        'occupation number': 6
    },
}
