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
Material data for hydrogen.

References
----------
Yong-Ki Kim, M.Eugene Rudd: Binary-encounter-dipole model for electron-impact ionization,
Phys.Rev.A 50, No.5, 1994
"""

binding_energy = 13.6057

# Include 0th order = 0.
dipole_oscillator_strength_coefficients = [
    0.,
    0.,
    -2.2473e-2,
    1.1775,
    -4.6264e-1,
    8.9064e-2,
    0.,
    0.]

effective_charge = 1.0
