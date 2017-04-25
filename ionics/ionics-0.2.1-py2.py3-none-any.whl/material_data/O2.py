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
Material data for molecular oxygen.

References
----------
(1) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.445, TABLE I)
"""

orbitals = {  # Ref.(1)
    '1sigma_g': {
        'binding energy': 543.5,
        'average kinetic energy': 794.84,
        'occupation number': 2
    },
    '1sigma_u': {
        'binding energy': 543.5,
        'average kinetic energy': 795.06,
        'occupation number': 2
    },
    '2sigma_g': {
        'binding energy': 40.3,
        'average kinetic energy': 78.19,
        'occupation number': 2
    },
    '2sigma_u': {
        'binding energy': 25.69,
        'average kinetic energy': 90.40,
        'occupation number': 2
    },
    '1pi_u': {
        'binding energy': 18.88,
        'average kinetic energy': 72.24,
        'occupation number': 4
    },
    '3sigma_g': {
        'binding energy': 16.42,
        'average kinetic energy': 60.08,
        'occupation number': 2
    },
    '1pi_g': {
        'binding energy': 12.07,
        'average kinetic energy': 82.14,
        'occupation number': 2
    },
}
