# This file is part of xrayutilities.
#
# xrayutilities is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2017 Dominik Kriegner <dominik.kriegner@gmail.com>

import xrayutilities as xu
import numpy
from matplotlib.pylab import *
from scipy.constants import physical_constants

asio = 3.975
asto = xu.materials.SrTiO3.a

class DarwinModelSTOSIO(xu.simpack.DarwinModelAlloy):
    """
    Darwin theory of diffraction for a binary alloy system.
    The model is based on separation of the sample structure into building
    blocks of atomic planes from which a multibeam dynamical model is
    calculated.
    """
    re = physical_constants['classical electron radius'][0] * 1e10
    asub = asto

    @classmethod
    def abulk(cls, x):
        """
        calculate the bulk (relaxed) lattice parameter of the SrIr{x}Ti_{1-x}O3
        alloy
        """
        return asto + (asio - asto)*x

    @classmethod
    def poisson_ratio(cls, x):
        """
        calculate the Poisson ratio of the alloy
        """
        return 0.6 # roughly from http://aip.scitation.org/doi/10.1063/1.4919837

    def get_dperp_apar(cls, x, apar, r=1):
        """
        calculate inplane lattice parameter and the out of plane lattice plane
        spacing (of the atomic planes!) from composition and relaxation

        Parameters
        ----------
         x:     chemical composition parameter
         apar:  inplane lattice parameter of the material below the current
                layer (onto which the present layer is strained to). This value
                also served as a reference for the relaxation parameter.
         r:     relaxation parameter. 1=relaxed, 0=pseudomorphic

        Returns
        -------
         dperp, apar
        """
        abulk = cls.abulk(x)
        aparl = apar + (abulk - apar) * r
        dperp = abulk*(1+cls.poisson_ratio(x)*(1-aparl/abulk))/2.0
        return dperp, aparl

    def init_structurefactors(self, temp=300):
        """
        calculates the needed atomic structure factors

        Parameters (optional)
        ---------------------
         temp:      temperature used for the Debye model
        """
        en = self.exp.energy
        q = numpy.sqrt(self.qinp[0]**2 + self.qinp[1]**2 + self.qz**2)
        self.fSr = xu.materials.elements.Sr.f(q, en)
        self.fTi = xu.materials.elements.Ti.f(q, en)
        self.fIr = xu.materials.elements.Ir.f(q, en)
        self.fO = xu.materials.elements.O.f(q, en)
        self.fSr0 = xu.materials.elements.Sr.f(0, en)
        self.fTi0 = xu.materials.elements.Ti.f(0, en)
        self.fIr0 = xu.materials.elements.Ir.f(0, en)
        self.fO0 = xu.materials.elements.O.f(0, en)

    def _calc_mono(self, pdict, pol):
        """
        calculate the reflection and transmission coefficients of monolayer

        Parameters
        ----------
         pdict: property dictionary, contains the layer properties:
           x:   Al-content of the layer (0: SrTiO3, 1: SrIrO3)
         pol:   polarization of the x-rays (either 'S' or 'P')

        Returns
        -------
         r, rbar, t: reflection, backside reflection, and tranmission
                     coefficients
        """
        ainp = pdict.get('ai')
        typ = pdict.get('type')
        # pre-factor for reflection: contains footprint correction
        gamma = 4*numpy.pi * self.re/(self.qz*ainp**2)
        if typ == 'AO':
            r = -1j*gamma*self.C[pol] * (self.fSr + self.fO)
            t = 1 + 1j*gamma * (self.fSr0 + self.fO0)
        elif typ == 'BO2':
            x = pdict.get('x')
            r = -1j*gamma*self.C[pol] * (self.fTi + (self.fIr - self.fTi)*x + 2*self.fO)
            t = 1 + 1j*gamma * (self.fTi0 + (self.fIr0 - self.fTi0)*x + 2*self.fO0)
        return r, numpy.copy(r), t


mpl.rcParams['font.size'] = 16.0
en = 'CuKa1'
qz = linspace(0.01, 4.0, 5e3)

STO = xu.materials.SrTiO3
exp = xu.HXRD(STO.Q(1, 0, 0), STO.Q(0, 0, 1), en=en)
dm = DarwinModelSTOSIO(
    qz, experiment=exp, resolution_width=0.0005, I0=2e7, background=1e0)

dx=1.0
sideal = [(896286, [{'t': 1., 'x': 0, 'r': 0, 'type': 'AO'},
                    {'t': 1., 'x': 0, 'r': 0, 'type': 'BO2'},]),  # ~350um substrate
          (60, [{'t': 1, 'x': 0.5-dx/2, 'r': 0, 'type': 'AO'},
               {'t': 1, 'x': 0.5-dx/2, 'r': 0, 'type': 'BO2'},
               {'t': 1, 'x': 0.5+dx/2, 'r': 0, 'type': 'AO'},
               {'t': 1, 'x': 0.5+dx/2, 'r': 0, 'type': 'BO2'},]), # 60 period superlattice
         ]

dx=0.0
s2 = [(896286, [{'t': 1., 'x': 0, 'r': 0, 'type': 'AO'},
                {'t': 1., 'x': 0, 'r': 0, 'type': 'BO2'},]),  # ~350um substrate
      (60, [{'t': 1, 'x': 0.5-dx/2, 'r': 0, 'type': 'AO'},
            {'t': 1, 'x': 0.5-dx/2, 'r': 0, 'type': 'BO2'},
            {'t': 1, 'x': 0.5+dx/2, 'r': 0, 'type': 'AO'},
            {'t': 1, 'x': 0.5+dx/2, 'r': 0, 'type': 'BO2'},]), # 60 period superlattice
         ]



# perform Darwin-theory based simulation
mlideal = dm.make_monolayers(sideal)
Iideal = dm.simulate(mlideal)
ml2 = dm.make_monolayers(s2)
I2 = dm.simulate(ml2)

figure('XU-simpack (Darwin)', figsize=(10, 5))
clf()

subplot(121)
def convx(Q):
    return 2*numpy.degrees(numpy.arcsin(exp.wavelength*Q/(4*numpy.pi)))
#    return Q

semilogy(convx(qz), Iideal, 'r-', lw=2, label='ideal')
semilogy(convx(qz), I2, 'k-', lw=2, label='smeared')
ylim(0.5*dm.background, dm.I0)
xlim(convx(qz).min(), convx(qz).max())
plt.locator_params(axis='x', nbins=5)
#xlabel('Qz ($1/\AA$)')
xlabel('2Theta (deg)')
ylabel('Intensity (arb.u.)')
legend(fontsize='small')

subplot(122)
z, xAl = dm.prop_profile(mlideal, 'x')
plot(z/10, xAl, 'r-')
z, xAl = dm.prop_profile(mlideal, 'x')
plot(z/10, xAl, 'k-')
xlabel('depth z (nm)')
ylabel('Ir-content', color='m')
ylim(-0.05, 1.05)
twinx()
z, ai = dm.prop_profile(mlideal, 'ai')
plot(z/10, ai, 'b-')
xlim(-100, 3)
ylim(3.88, 4.0)
plt.locator_params(axis='x', nbins=5)
ylabel(r'a-inplane ($\AA$)', color='b')
tight_layout()
show()
