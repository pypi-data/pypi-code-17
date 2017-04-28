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
Material data for molecular nitrogen.

References
----------
(1) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions,
    Rev.Mod.Phys. 64, No.2, 1992 (p.457-461, section VI.C + p.445, TABLE I(a))
"""

kims_model_coefficients = {  # Ref.(1)
    'shells': [
        'L_A-shell',
        'L_B-shell',
        'K-shell'
    ],
    'L_A-shell': {
        'a_i': (5.5,   0.8,   3.4,  1.3,  1.6,  10.0),
        'b_i': (0.465, 0.59,  0.71, 0.81, 0.26, 0.11),
        'c_i': (0.155, 0.035, 0.14, 0.09, 0.08, 0.1),
        'd_i': (0.,    0.,    0.,   0.,   0.,   1.1),
        'f': 0.3,
        'g': -8.0,
        'h': 25.0,
        'k': 0.1,
        'p': 0.2,
        'binding energy': 15.59,
        'average kinetic energy': 44.27,
        'occupation number': 8,
    },
    'L_B-shell': {
        'a_i': (1.6,  0.7,   0.5,   0.5,  0.6,  0.4),
        'b_i': (0.26, 0.36,  0.525, 0.47, 0.12, 0.18),
        'c_i': (0.06, 0.055, 0.02,  0.08, 0.08, 0.05),
        'd_i': (0.,   0.,    2.0,   1.0,  0.1,  1.0),
        'f': 0.3,
        'g': -8.0,
        'h': 25.0,
        'k': 0.1,
        'p': 0.2,
        'binding energy': 28.8,  # This value is from TABLE IV and it disagrees with TABLE I(a)!
        'average kinetic energy': 69.53,
        'occupation number': 2,
    },
    'K-shell': {
        'e_i': (2.99, 5813, 30506, -1987000),
        'p': 0.2,
        'q': 1.0,
        'r': 0.1,
        'binding energy': 410.0,  # Corresponding value in TABLE I(a) is 409.9
        'average kinetic energy': (601.78+602.68)/2.,
        'occupation number': 4,
    },
}

orbitals = {  # Ref.(1)
    '1sigma_g': {
        'binding energy': 409.9,
        'average kinetic energy': 601.78,
        'occupation number': 2
    },
    '1sigma_u': {
        'binding energy': 409.9,
        'average kinetic energy': 602.68,
        'occupation number': 2
    },
    '2sigma_g': {
        'binding energy': 37.3,
        'average kinetic energy': 69.53,
        'occupation number': 2
    },
    '2sigma_u': {
        'binding energy': 18.78,
        'average kinetic energy': 62.45,
        'occupation number': 2
    },
    '1pi_u': {
        'binding energy': 16.96,
        'average kinetic energy': 55.21,
        'occupation number': 4
    },
    '3sigma_g': {
        'binding energy': 15.59,
        'average kinetic energy': 44.27,
        'occupation number': 2
    },
}
