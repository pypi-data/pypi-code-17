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

from numpy import sqrt, sin, log, exp, cos, arctan
import scipy.constants
from scipy.constants import physical_constants

import ionics.material_data as material_data


# noinspection PyPep8Naming
class VoitkivDDCS(object):
    """
    Double differential cross section for relativistic projectiles.

    References
    ----------
    A.B. Voitkiv, N. Gruen, W. Scheid: "Hydrogen and helium ionization by relativistic projectiles
    in collisions with small momentum transfer", J.Phys.B: At.Mol.Opt.Phys 32, 1999
    """

    def __init__(self, T0, Z0, material_id, unit='au'):
        """
        Parameters
        ----------
        T0 : float
            Projectile energy in units of [eV].
        Z0 : float or int
            Charge number of the projectile.
        material_id : str
            Specifies the target material (needs to be the name of a module in the subpackage
            :mod:`material_data`).
        unit : unicode
            Specifies the units in which the cross section values are returned; must be either
            ``'au'`` (atomic units) or ``'SI'`` ([m^2/eV]).
        """
        super(VoitkivDDCS, self).__init__()

        T0 = float(T0)
        Z0 = float(Z0)

        if unit == 'au':
            conversion_factor = 1
        elif unit == 'SI':
            conversion_factor = (physical_constants['atomic unit of length'][0]**2
                                 / (physical_constants['atomic unit of energy'][0]
                                    / physical_constants['elementary charge'][0]))
        else:
            raise ValueError('Invalid unit: %s (must be either "au" or "SI"' % unit)

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        self.Zt = Zt = material.effective_charge

        T0 /= 1.0e6  # [eV] -> [MeV]
        gamma = T0 / physical_constants['proton mass energy equivalent in MeV'][0] + 1.
        beta = 1. - (1. / gamma ** 2)

        # Use atomic units.
        c_au = (physical_constants['speed of light in vacuum'][0]
                / physical_constants['atomic unit of velocity'][0])
        v_au = beta * c_au

        b_min = max(1., Z0 / v_au)

        self.prefactor = conversion_factor * 2 ** 9 * Z0 ** 2 / (v_au * Zt ** 2) ** 2
        self.term1_prefactor = 1.
        self.term2_prefactor = 1. / gamma ** 2
        self.term3_prefactor = -0.5
        self.term4_prefactor = sqrt(128.) / v_au * (1. - beta ** 2 / 2.)
        self.term5_prefactor = 2. * Z0 * Zt / (v_au * gamma) ** 2
        self.eta_part1 = log(2.246 * v_au * gamma / (b_min * Zt))

    def __call__(self, W, T):
        """
        Evaluate the double differential ionization cross section for the given energy and
        scattering angle.

        Parameters
        ----------
        W : float
            Kinetic energy of the ionized electron in units of [eV].
        T : float
            (Polar) scattering angle in units of [rad]; T = 0 is the direction of
            the projectile's velocity.

        Returns
        -------
        value : float
            The value of the ionization cross section.
        """
        pi = scipy.constants.pi

        # Use atomic units
        W_au = (W * physical_constants['elementary charge'][0]
                / physical_constants['atomic unit of energy'][0])

        EZt2 = 2. * W_au / self.Zt ** 2
        EZt2sqrt = sqrt(EZt2)

        logeta = self.eta_part1 - log(1. + EZt2)

        return (
            self.prefactor
            * 1. / (1. + EZt2) ** 5
            * exp(-4. * arctan(EZt2sqrt) / EZt2sqrt) / (1. - exp(-2. * pi / EZt2sqrt))
            * (
                self.term1_prefactor * sin(T) ** 2 * logeta
                + self.term2_prefactor * cos(T) ** 2
                + self.term3_prefactor * sin(T) ** 2
                + self.term4_prefactor * sqrt(W_au) * cos(T) * sin(T) ** 2 * logeta
                + self.term5_prefactor * cos(T) * logeta ** 2
            )
        )


cross_sections = (VoitkivDDCS,)
