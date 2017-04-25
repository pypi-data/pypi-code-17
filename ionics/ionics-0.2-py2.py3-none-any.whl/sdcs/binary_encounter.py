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
Various cross sections in the binary encounter approximation.
"""

import scipy.constants
from scipy.constants import physical_constants
from numpy import array
from numpy import sqrt
import ionics.material_data as material_data


# noinspection PyPep8Naming
class ModifiedRutherfordCrossSection(object):
    """
    Single differential cross section with respect to energy in the binary encounter approximation.

    References
    ----------
    (1) M.E.Rudd, Y.-K.Kim, D.H.Madison, T.J.Gay: "Electron production in proton collisions with
    atoms and molecules: energy distributions", Rev.Mod.Phys. Vol.64 No.2, 1992 [p.448-449]
    """

    def __init__(self, T0, material_id):
        """
        Parameters
        ----------
        T0 : float
            Projectile energy per nucleon in units of [eV].
        material_id : str
            Specifies the target material (needs to be the name of a module in the subpackage
            :mod:`material_data`).
        """
        super(ModifiedRutherfordCrossSection, self).__init__()

        T0 = float(T0)

        self.T = T0 / physical_constants['proton-electron mass ratio'][0]

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        self.B = material.binding_energy
        try:
            # Use only the outermost shell.
            self.U = material.electron_average_kinetic_energies.values()[-1]
        except AttributeError:
            # If not available, compute kinetic energy from virial theorem.
            self.U = self.B/2.

        self.E_minus = 4.*self.T - 4.*sqrt(self.T*self.U)
        self.E_plus = 4.*self.T + 4.*sqrt(self.T*self.U)

        a0 = physical_constants['Bohr radius'][0]
        R = physical_constants['Rydberg constant times hc in eV'][0]
        pi = scipy.constants.pi
        # This is the prefactor from the original Rutherford cross section.
        self.prefactor = 4 * pi * a0**2 / self.T * R**2

    def __call__(self, W):
        """
        Evaluate the single differential ionization cross section at the given energy.

        Parameters
        ----------
        W : float
            Kinetic energy of the ionized electron in units of [eV].

        Returns
        -------
        value : float
            The value of the ionization cross section.
        """
        E = W + self.B
        if isinstance(E, float):
            return self._compute(E)
        else:
            # E is a numpy.ndarray.
            # noinspection PyTypeChecker
            return array([self._compute(e) for e in E])

    def _compute(self, E):
        """
        Compute the value of the ionization cross section for the given energy loss.

        Parameters
        ----------
        E : float
            Energy loss of projectile in units of [eV].

        Returns
        -------
        value : float
            The value of the ionization cross section.
        """
        T = self.T
        U = self.U
        if E > self.E_plus:
            return 0.
        elif E > self.E_minus:
            return self.prefactor * U / (6. * E**3) * (
                    sqrt(4.*T/U)**3 + (1. - sqrt(1. + E/U))**3
                   )
        else:
            # Actually should define E_min and check if E > E_min,
            # here E_min = B is assumed => W > 0;
            # Refer to p.449 of Rudd 1992.
            return self.prefactor * 1./E**2 * (1. + 4.*U/(3.*E))


cross_sections = (ModifiedRutherfordCrossSection,)
