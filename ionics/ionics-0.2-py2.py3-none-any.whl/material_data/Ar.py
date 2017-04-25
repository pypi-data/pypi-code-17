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
Material data for argon.

References
----------
(1) Rudd, Kim, Madison, Gay: "Electron production in proton collisions with atoms and molecules:
    energy distributions",
    Rev.Mod.Phys. 64, No.2, 1992 (p.457-461, section VI.C + p.445, TABLE I(a))
"""

kims_model_coefficients = {  # Ref.(1)
    'shells': [
        'M-shell',
        'L-shell'
    ],
    'M-shell': {
        'a_i': (7.0,   12.0, 0.3,  11.3, 10.0),
        'b_i': (0.505, 0.07, 0.6,  0.72, 0.63),
        'c_i': (0.12,  0.13, 0.05, 0.19, 0.1),
        'd_i': (0.01,  1.0,  1.0,  3.0,  3.0),
        'f': 0.053,
        'g': -5.0,
        'h': 20.0,
        'k': 0.1,
        'p': 0.3,
        'binding energy': 15.82,
        'average kinetic energy': 78.07,
        'occupation number': 8,
    },
    'L-shell': {
        'e_i': (48.67, 745.6, -141200.0, 616300.0),
        # The p-value for the L-shell is actually missing in the paper
        # (assume same values as for M-shell).
        'p': 0.3,
        'q': 0.25,
        'r': 0.1,
        'binding energy': 249.18,
        'average kinetic energy': 651.4,
        'occupation number': 8,
    },
}

shells = {  # Ref.(1)
    '1s': {
        'binding energy': 3202.9,
        'average kinetic energy': 4192.9,
        'occupation number': 2
    },
    '2s': {
        'binding energy': 326.0,
        'average kinetic energy': 683.1,
        'occupation number': 2
    },
    '2p': {
        'binding energy': 249.18,
        'average kinetic energy': 651.4,
        'occupation number': 6
    },
    '3s': {
        'binding energy': 29.24,
        'average kinetic energy': 103.5,
        'occupation number': 2
    },
    '3p': {
        'binding energy': 15.82,
        'average kinetic energy': 78.07,
        'occupation number': 6
    },
}
