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
Material data for neon.

References
----------
(1) Rudd, Kim, Madison, Gay: Electron production in proton collisions with atoms and molecules:
    energy distributions, Rev.Mod.Phys. 64, No.2, 1992 (p.445, TABLE I)
(2) E.Clementi, D.L.Raimondi, W.P.Reinhardt: Atomic Screening Constants from SCF Functions,
    J.Chem.Phys.38, No.11, pp.2686-2689, 1963
"""

effective_charge = 5.758  # Ref.(2)

shells = {  # Ref.(1)
    '1s': {
        'binding energy': 866.9,
        'average kinetic energy': 1259.1,
        'occupation number': 2
    },
    '2s': {
        'binding energy': 48.47,
        'average kinetic energy': 141.88,
        'occupation number': 2
    },
    '2p': {
        'binding energy': 21.60,
        'average kinetic energy': 116.02,
        'occupation number': 6
    },
}
