# -*- coding: utf-8 -*-

#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2017  The IPMSim collaboration <http://ipmsim.gitlab.io/IPMSim>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

from scipy.constants import physical_constants

from virtual_ipm.components import Mutable
from virtual_ipm.utils import to_json_string


class ParticleType(Mutable):
    """
    This class represents a particle type.
    """
    def __init__(self, charge, charge_number, mass, rest_energy):
        """
        Parameters
        ----------
        charge : float
            Electric charge in units of [C].
        charge_number : int
            Electric charge in units of [elementary charge].
        mass : float
            Mass in units of [kg].
        rest_energy : float
            Rest energy in units of [eV].
        """
        super(ParticleType, self).__init__()
        self.charge = charge
        self.charge_number = charge_number
        self.mass = mass
        self.rest_energy = rest_energy

    def __str__(self):
        return to_json_string(self.as_json())

    def as_json(self):
        return {
            'charge': self.charge,
            'charge_number': self.charge_number,
            'mass': self.mass,
            'rest_energy': self.rest_energy,
        }


Electron = ParticleType(
    -1.0 * physical_constants['elementary charge'][0],
    -1,
    physical_constants['electron mass'][0],
    physical_constants['electron mass energy equivalent in MeV'][0] * 1.0e6
)

Proton = ParticleType(
    physical_constants['elementary charge'][0],
    1,
    physical_constants['proton mass'][0],
    physical_constants['proton mass energy equivalent in MeV'][0] * 1.0e6
)
