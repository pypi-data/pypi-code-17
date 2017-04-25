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
Various cross sections using the Bethe approximation.
"""

from numpy import exp, log, poly1d
import scipy.constants
from scipy.constants import physical_constants

import ionics.material_data as material_data


# noinspection PyPep8Naming
class BetheNonRel(object):
    """
    Non relativistic formulation of the single differential cross section in
    the Bethe approximation.

    References
    ----------
    (1) J.H.Miller, L.H.Toburen: "Differential cross sections for ionization of helium, neon and
        argon by high-velocity ions", Phys.Rev.A 27, No.3, 1983
    (2) Yong-Ki Kim, M.Eugene Rudd: "Binary-encounter-dipole model for electron-impact ionization",
        Phys.Rev.A 50, No.5, 1994
    """

    def __init__(self, T0, N, material_id):
        """
        Parameters
        ----------
        T0 : float
            Projectile energy per nucleon in units of [eV].
        N : int
            Charge number of the projectiles.
        material_id : str
            Specifies the target material (needs to be the name of a module in the subpackage
            :mod:`material_data`).
        """
        super(BetheNonRel, self).__init__()

        T0 = float(T0)
        N = float(N)
        material_id = str(material_id)

        T = T0 / physical_constants['proton-electron mass ratio'][0]
        z = N

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        self.B = material.binding_energy
        self.dpos = poly1d(material.dipole_oscillator_strength_coefficients)

        a0 = physical_constants['Bohr radius'][0]
        R = physical_constants['Rydberg constant times hc in eV'][0]
        pi = scipy.constants.pi

        self.prefactor = 4. * pi * a0**2 * z**2 * R**2 / T * 2.
        self.term1 = log(4. * R * T) / 2.

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
        # E: Total energy needed for ionization, energy loss of projectile.
        E = W + self.B
        dipole_oscillator_strength = self.dpos(self.B / E)
        return self.prefactor * dipole_oscillator_strength / E * (self.term1 - log(E))


class BetheRel(object):
    """
    Relativistic formulation of the single differential cross section in the Bethe approximation.

    References
    ----------
    (1) M.E.Rudd, Y.-K. Kim, D.H.Madison, T.J. Gay: "Electron production in proton collisions with
        atoms and molecules: energy distributions", Rev.Mod.Phys. 64, 1992
    (2) Yong-Ki Kim, M.Eugene Rudd: "Binary-encounter-dipole model for electron-impact ionization",
        Phys.Rev.A 50, No.5, 1994
    """

    # noinspection PyPep8Naming
    def __init__(self, T0, N, material_id):
        """
        Parameters
        ----------
        T0 : float
            Projectile energy per nucleon in units of [eV].
        N : int
            Charge number of the projectiles.
        material_id : str
            Specifies the target material (needs to be the name of a module in the subpackage
            :mod:`material_data`).
        """
        super(BetheRel, self).__init__()

        T0 = float(T0)
        N = float(N)

        T0 /= 1.0e6  # [eV] -> [MeV]
        gamma = T0 / physical_constants['proton mass energy equivalent in MeV'][0] + 1.
        beta = 1. - 1. / gamma ** 2
        z = N

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        self.B = material.binding_energy
        self.dpos = poly1d(material.dipole_oscillator_strength_coefficients)

        a0 = physical_constants['Bohr radius'][0]
        R = physical_constants['Rydberg constant times hc in eV'][0]
        pi = scipy.constants.pi
        alpha = physical_constants['fine-structure constant'][0]

        self.prefactor = 4. * pi * a0**2 * z**2 * alpha**2 * R / beta**2 * 2.
        self.term1 = log(gamma * beta) - beta ** 2 / 2. + log(R / alpha)

    # noinspection PyPep8Naming
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
        # E: Total energy needed for ionization, energy loss of projectile.
        E = W + self.B
        dipole_oscillator_strength = self.dpos(self.B / E)
        return self.prefactor * dipole_oscillator_strength / E * (self.term1 - log(E))


# noinspection PyPep8Naming
class BetheAfterInokuti(object):
    """
    Non relativistic version of the Bethe formulation. Generalized oscillator strengths fitted to
    a power series are used.

    References
    ----------
    (1) Inokuti, Dillon, Miller, Omidvar: "Analytic representation of secondary-electron spetra",
        J.Chem.Phys. 87 (12), 1987
    """

    def __init__(self, T0, N0, material_id):
        """
        Parameters
        ----------
        T0 : float
            Projectile energy per nucleon in units of [eV].
        N0 : int
            Charge number of the projectile.
        material_id : str
            Specifies the target material (needs to be the name of a module in the subpackage
            :mod:`material_data`).
        """
        super(BetheAfterInokuti, self).__init__()

        T0 = float(T0)
        N0 = float(N0)

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        T = T0 / physical_constants['proton-electron mass ratio'][0]

        a0 = physical_constants['Bohr radius'][0]
        pi = scipy.constants.pi

        self.prefactor = 4. * pi * a0**2 * N0**2 / T
        self.log_T = log(T)

        self.a_i = material.coefficients_for_Bethe_after_Inokuti['a_i']
        self.b_i = material.coefficients_for_Bethe_after_Inokuti['b_i']

        self.shells = material.shells.values()

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
        dsdw = 0.
        for shell in self.shells:
            E = W + shell['binding energy']
            A = self._compute_A_B(W, E, self.a_i)
            B = self._compute_A_B(W, E, self.b_i)
            dsdw += (A * self.log_T + B) * shell['occupation number']
        return self.prefactor * dsdw

    # noinspection PyMethodMayBeStatic
    def _compute_A_B(self, W, E, coefficients):
        """
        Compute the generalized oscillator strength for the given coefficients.

        Parameters
        ----------
        W : float
            Electron kinetic energy in units of [eV].
        E : float
            Energy loss of projectile in units of [eV].
        coefficients : list or tuple
            The coefficients for the power series for either ``A`` or ``B``.

        Returns
        -------
        gos : float
            The generalized oscillator strength.
        """
        g = W / E
        A_B = 0.
        for i, c in enumerate(coefficients):
            A_B += c * g**i
        return A_B * (1. - g)**2


# noinspection PyPep8Naming
class KimsModel(object):
    """
    Non-relativistic single differential cross section with respect to energy, based on
    the Bethe formulation.

    References
    ----------
    (1) Rudd, Kim, Madison, Gay: "Electron production in proton collisions with atoms and
        molecules: energy distributions", Rev.Mod.Phys. 64, No.2, 1992 (p.457-461, section VI.C)
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
        super(KimsModel, self).__init__()

        T0 = float(T0)

        try:
            material = getattr(material_data, material_id)
        except AttributeError:
            raise ValueError('Unknown material: %s' % material_id)

        self.shell_coefficients = material.kims_model_coefficients

        self.T = T = T0 / physical_constants['proton-electron mass ratio'][0]

        a0 = physical_constants['Bohr radius'][0]
        pi = scipy.constants.pi
        self.R = R = physical_constants['Rydberg constant times hc in eV'][0]

        self.rutherford_prefactor = 4.*pi*a0**2 / T * R**2

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
        shell_sum = 0.
        for shell in self.shell_coefficients['shells']:
            coefficients = self.shell_coefficients[shell]
            rutherford_cross_section = (
                self.rutherford_prefactor / (coefficients['binding energy'] + W)**2
            )
            if 'f' in coefficients:
                shell_sum += self._compute_Y_M(W, coefficients) * rutherford_cross_section
            elif 'q' in coefficients:
                shell_sum += self._compute_Y_L(W, coefficients) * rutherford_cross_section
            else:
                raise AttributeError(
                    'Insufficient material data (found neither "f" nor "q" coefficient'
                )
        return shell_sum

    # noinspection PyMethodMayBeStatic
    def _compute_Y_BE(self, W, coefficients):
        """
        Parameters
        ----------
        W : float
            Electron kinetic energy in units of [eV].
        coefficients : dict
            The coefficients for the respective shell.

        Returns
        -------
        float
        """
        N = coefficients['occupation number']
        U = coefficients['average kinetic energy']
        E = W + coefficients['binding energy']
        p = coefficients['p']
        return N * U / E * (1. - (U / (W + U))**p)

    def _compute_Y_M(self, W, coefficients):
        """
        Parameters
        ----------
        W : float
            Electron kinetic energy in units of [eV].
        coefficients : dict
            The coefficients for the respective shell.

        Returns
        -------
        float
        """
        E = W + coefficients['binding energy']

        R = self.R
        T = self.T

        f = coefficients['f']
        g = coefficients['g']
        h = coefficients['h']
        k = coefficients['k']

        N = coefficients['occupation number']

        EdfdE = self._compute_continuum_oscillator_strength_gaussian(E, coefficients)
        term1 = EdfdE * log(4.*f*T/R) * (1. + g*R/T + h*R**2/T**2)
        Y_BE = self._compute_Y_BE(W, coefficients)
        denominator = 1. + exp(k * (E - 4.*T) / R)

        return (term1 + Y_BE + N) / denominator

    def _compute_Y_L(self, W, coefficients):
        """
        Parameters
        ----------
        W : float
            Electron kinetic energy in units of [eV].
        coefficients : dict
            The coefficients for the respective shell.

        Returns
        -------
        float
        """
        E = W + coefficients['binding energy']

        R = self.R
        T = self.T

        q = coefficients['q']
        r = coefficients['r']

        N = coefficients['occupation number']

        EdfdE = self._compute_continuum_oscillator_strength_power_series(E, coefficients)
        term1 = EdfdE * log(4.*q*T*E/R**2)
        Y_BE = self._compute_Y_BE(W, coefficients)
        denominator = 1. + exp(r * (E - 4.*T) / R)

        return (term1 + Y_BE + N) / denominator

    def _compute_continuum_oscillator_strength_gaussian(self, E, coefficients):
        """
        Parameters
        ----------
        E : float
            Energy loss of projectile in units of [eV].
        coefficients : dict
            The coefficients for the respective shell.

        Returns
        -------
        float
        """
        R = self.R
        EdfdE = 0.
        for a, b, c, d in zip(
                coefficients['a_i'],
                coefficients['b_i'],
                coefficients['c_i'],
                coefficients['d_i']
        ):
            EdfdE += a * exp(-((R/E - b) / c)**2) * (R / E)**d
        return EdfdE

    def _compute_continuum_oscillator_strength_power_series(self, E, coefficients):
        """
        Parameters
        ----------
        E : float
            Energy loss of projectile in units of [eV].
        coefficients : dict
            The coefficients for the respective shell.

        Returns
        -------
        float
        """
        R = self.R
        EdfdE = 0.
        for i, e in enumerate(coefficients['e_i']):
            EdfdE += e * (R / E) ** (i + 1)
        return EdfdE


cross_sections = (BetheNonRel, BetheRel, BetheAfterInokuti, KimsModel)
