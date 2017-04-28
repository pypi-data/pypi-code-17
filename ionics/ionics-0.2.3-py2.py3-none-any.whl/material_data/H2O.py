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
Material data for water.

References
----------
(1) Inokuti, Dillon, Miller, Omidvar: Analytic representation of secondary-electron spetra,
    J.Chem.Phys. 87 (12), 1987
(2) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.447, TABLE I(b))
"""

coefficients_for_Bethe_after_Inokuti = {  # Ref.(1)
    'a_i': ( 0.323,  38.61, -157.3,   311.2, -296.4,   103.7),
    'b_i': (-0.564, -208.5,  1006.0, -1990.0, 1849.0, -646.8),
}

shells = {  # Ref.(2)
    '1a_1': {
        'binding energy': 539.7,
        'average kinetic energy': 1589.5,
        'occupation number': 2
    },
    '2a_1': {
        'binding energy': 32.2,
        'average kinetic energy': 142.0,
        'occupation number': 2
    },
    '1b_1': {
        'binding energy': 18.55,
        'average kinetic energy': 97.39,
        'occupation number': 2
    },
    '3a_1': {
        'binding energy': 14.73,
        'average kinetic energy': 118.4,
        'occupation number': 2
    },
    '1b_2': {
        'binding energy': 12.61,
        'average kinetic energy': 122.9,
        'occupation number': 2
    },
}
