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
Material data for helium.

References
----------
(1) Yong-Ki Kim, M.Eugene Rudd: Binary-encounter-dipole model for electron-impact ionization,
    Phys.Rev.A 50, No.5, 1994
(2) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.445, TABLE I)
"""

binding_energy = 24.587
electron_average_kinetic_energies = [39.51]  # [eV]

# Include 0th order = 0.
dipole_oscillator_strength_coefficients = [  # Ref.(1)
    0.,
    0.,
    0.,
    1.2178e1,
    -2.9585e1,
    3.1251e1,
    -1.2175e1,
    0.
]

effective_charge = 1.5

shells = {  # Ref.(2)
    '1s': {
        'binding energy': 24.59,
        'average kinetic energy': 39.51,
        'occupation number': 2
    },
}
