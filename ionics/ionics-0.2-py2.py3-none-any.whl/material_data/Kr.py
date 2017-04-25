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
Material data for krypton.

References
----------
(1) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.445, TABLE I)
"""

shells = {  # Ref.(1)
    '1s': {
        'binding energy': 14.3256e3,
        'average kinetic energy': 17.1461e3,
        'occupation number': 2
    },
    '2s': {
        'binding energy': 1921.0,
        'average kinetic energy': 3406.9,
        'occupation number': 2
    },
    '2p': {
        'binding energy': 1692.3,
        'average kinetic energy': 3375.0,
        'occupation number': 6
    },
    '3s': {
        'binding energy': 295.2,
        'average kinetic energy': 829.8,
        'occupation number': 2
    },
    '3p': {
        'binding energy': 216.8,
        'average kinetic energy': 773.7,
        'occupation number': 6
    },
    '3d': {
        'binding energy': 93.0,
        'average kinetic energy': 650.3,
        'occupation number': 10
    },
    '4s': {
        'binding energy': 27.5,
        'average kinetic energy': 115.8,
        'occupation number': 2
    },
    '4p': {
        'binding energy': 14.22,
        'average kinetic energy': 82.72,
        'occupation number': 6
    },
}
