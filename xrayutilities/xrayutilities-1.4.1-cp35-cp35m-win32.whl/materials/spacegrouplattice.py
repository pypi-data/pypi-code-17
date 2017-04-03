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
"""
module handling crystal lattice structures. A SGLattice consists of a space
group number and the position of atoms specified as Wyckoff positions along
with their parameters. Depending on the space group symmetry only certain
parameters of the resulting instance will be settable! A cubic lattice for
example allows only to set its 'a' lattice parameter but none of the other unit
cell shape parameters.
"""
from __future__ import division

import numbers
import sys
from collections import OrderedDict
from math import cos, degrees, radians, sin, sqrt

import numpy

from . import elements
from .. import config, math
from ..exception import InputError
from .atom import Atom
from .wyckpos import wp

if sys.version_info < (3, 0):
    range = xrange


class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
        else:
            return super(RangeDict, self).__getitem__(item)

# space group number to symmetry and number of parameters dictionary
sgrp_sym = RangeDict({range(1, 3): ('triclinic', 6),
                      range(3, 16): ('monoclinic', 4),
                      range(16, 75): ('orthorhombic', 3),
                      range(75, 143): ('tetragonal', 2),
                      range(143, 168): ('trigonal', 2),
                      range(168, 195): ('hexagonal', 2),
                      range(195, 231): ('cubic', 1)})

sgrp_name = {'1': 'P1', '2': 'P-1', '3': 'P2', '4': 'P21', '5': 'C2',
             '6': 'Pm', '7': 'Pc', '8': 'Cm', '9': 'Cc', '10': 'P2/m',
             '11': 'P21/m', '12': 'C2/m', '13': 'P2/c', '14': 'P21/c',
             '15': 'C2/c', '16': 'P222', '17': 'P2221', '18': 'P21212',
             '19': 'P212121', '20': 'C2221', '21': 'C222', '22': 'F222',
             '23': 'I222', '24': 'I212121', '25': 'Pmm2', '26': 'Pmc21',
             '27': 'Pcc2', '28': 'Pma2', '29': 'Pca21', '30': 'Pnc2',
             '31': 'Pmn21', '32': 'Pba2', '33': 'Pna21', '34': 'Pnn2',
             '35': 'Cmm2', '36': 'Cmc21', '37': 'Ccc2', '38': 'Amm2',
             '39': 'Aem2', '40': 'Ama2', '41': 'Aea2', '42': 'Fmm2',
             '43': 'Fdd2', '44': 'Imm2', '45': 'Iba2', '46': 'Ima2',
             '47': 'Pmmm', '48': 'Pnnn', '49': 'Pccm', '50': 'Pban',
             '51': 'Pmma', '52': 'Pnna', '53': 'Pmna', '54': 'Pcca',
             '55': 'Pbam', '56': 'Pccn', '57': 'Pbcm', '58': 'Pnnm',
             '59': 'Pmmn', '60': 'Pbcn', '61': 'Pbca', '62': 'Pnma',
             '63': 'Cmcm', '64': 'Cmce', '65': 'Cmmm', '66': 'Cccm',
             '67': 'Cmme', '68': 'Ccce', '69': 'Fmmm', '70': 'Fddd',
             '71': 'Immm', '72': 'Ibam', '73': 'Ibca', '74': 'Imma',
             '75': 'P4', '76': 'P41', '77': 'P42', '78': 'P43',
             '79': 'I4', '80': 'I41', '81': 'P-4', '82': 'I-4',
             '83': 'P4/m', '84': 'P42/m', '85': 'P4/n', '86': 'P42/n',
             '87': 'I4/m', '88': 'I41/a', '89': 'P422', '90': 'P4212',
             '91': 'P4122', '92': 'P41212', '93': 'P4222', '94': 'P42212',
             '95': 'P4322', '96': 'P43212', '97': 'I422', '98': 'I4122',
             '99': 'P4mm', '100': 'P4bm', '101': 'P42cm', '102': 'P42nm',
             '103': 'P4cc', '104': 'P4nc', '105': 'P42mc', '106': 'P42bc',
             '107': 'I4mm', '108': 'I4cm', '109': 'I41md', '110': 'I41cd',
             '111': 'P-42m', '112': 'P-42c', '113': 'P-421m',
             '114': 'P-421c', '115': 'P-4m2', '116': 'P-4c2',
             '117': 'P-4b2', '118': 'P-4n2', '119': 'I-4m2',
             '120': 'I-4c2', '121': 'I-42m', '122': 'I-42d',
             '123': 'P4/mmm', '124': 'P4/mcc', '125': 'P4/nbm',
             '126': 'P4/nnc', '127': 'P4/mbm', '128': 'P4/mnc',
             '129': 'P4/nmm', '130': 'P4/ncc', '131': 'P42/mmc',
             '132': 'P42/mcm', '133': 'P42/nbc', '134': 'P42/nnm',
             '135': 'P42/mbc', '136': 'P42/mnm', '137': 'P42/nmc',
             '138': 'P42/ncm', '139': 'I4/mmm', '140': 'I4/mcm',
             '141': 'I41/amd', '142': 'I41/acd', '143': 'P3',
             '144': 'P31', '145': 'P32', '146': 'R3', '147': 'P-3',
             '148': 'R-3', '149': 'P312', '150': 'P321', '151': 'P3112',
             '152': 'P3121', '153': 'P3212', '154': 'P3221', '155': 'R32',
             '156': 'P3m1', '157': 'P31m', '158': 'P3c1', '159': 'P31c',
             '160': 'R3m', '161': 'R3c', '162': 'P-31m', '163': 'P-31c',
             '164': 'P-3m1', '165': 'P-3c1', '166': 'R-3m', '167': 'R-3c',
             '168': 'P6', '169': 'P61', '170': 'P65', '171': 'P62',
             '172': 'P64', '173': 'P63', '174': 'P-6', '175': 'P6/m',
             '176': 'P63/m', '177': 'P622', '178': 'P6122',
             '179': 'P6522', '180': 'P6222', '181': 'P6422',
             '182': 'P6322', '183': 'P6mm', '184': 'P6cc', '185': 'P63cm',
             '186': 'P63mc', '187': 'P-6m2', '188': 'P-6c2',
             '189': 'P-62m', '190': 'P-62c', '191': 'P6/mmm',
             '192': 'P6/mcc', '193': 'P63/mcm', '194': 'P63/mmc',
             '195': 'P23', '196': 'F23', '197': 'I23', '198': 'P213',
             '199': 'I213', '200': 'Pm-3', '201': 'Pn-3', '202': 'Fm-3',
             '203': 'Fd-3', '204': 'Im-3', '205': 'Pa-3', '206': 'Ia-3',
             '207': 'P432', '208': 'P4232', '209': 'F432',
             '210': 'F4132', '211': 'I432', '212': 'P4332',
             '213': 'P4132', '214': 'I4132', '215': 'P-43m',
             '216': 'F-43m', '217': 'I-43m', '218': 'P-43n',
             '219': 'F-43c', '220': 'I-43d', '221': 'Pm-3m',
             '222': 'Pn-3n', '223': 'Pm-3n', '224': 'Pn-3m',
             '225': 'Fm-3m', '226': 'Fm-3c', '227': 'Fd-3m',
             '228': 'Fd-3c', '229': 'Im-3m', '230': 'Ia-3d'}

sgrp_params = {'cubic:1': (('a', ), ('a', 'a', 'a', 90, 90, 90)),
               'cubic:2': (('a', ), ('a', 'a', 'a', 90, 90, 90)),
               'cubic': (('a', ), ('a', 'a', 'a', 90, 90, 90)),
               'hexagonal': (('a', 'c'), ('a', 'a', 'c', 90, 90, 120)),
               'trigonal:R': (('a', 'alpha'), ('a', 'a', 'a', 'alpha',
                                               'alpha', 'alpha')),
               'trigonal:H': (('a', 'c'), ('a', 'a', 'c', 90, 90, 120)),
               'trigonal': (('a', 'c'), ('a', 'a', 'c', 90, 90, 120)),
               'tetragonal:1': (('a', 'c'), ('a', 'a', 'c', 90, 90, 90)),
               'tetragonal:2': (('a', 'c'), ('a', 'a', 'c', 90, 90, 90)),
               'tetragonal': (('a', 'c'), ('a', 'a', 'c', 90, 90, 90)),
               'orthorhombic:1': (('a', 'b', 'c'),
                                  ('a', 'b', 'c', 90, 90, 90)),
               'orthorhombic:2': (('a', 'b', 'c'),
                                  ('a', 'b', 'c', 90, 90, 90)),
               'orthorhombic': (('a', 'b', 'c'),
                                ('a', 'b', 'c', 90, 90, 90)),
               'monoclinic:b': (('a', 'b', 'c', 'beta'),
                                ('a', 'b', 'c', 90, 'beta', 90)),
               'monoclinic:c': (('a', 'b', 'c', 'gamma'),
                                ('a', 'b', 'c', 90, 90, 'gamma')),
               'monoclinic': (('a', 'b', 'c', 'beta'),
                              ('a', 'b', 'c', 90, 'beta', 90)),
               'triclinic': (('a', 'b', 'c', 'alpha', 'beta', 'gamma'),
                             ('a', 'b', 'c', 'alpha', 'beta', 'gamma'))}


class WyckoffBase(list):

    """
    The WyckoffBase class implements a container for a set of Wyckoff positions
    that form the base of a crystal lattice. An instance of this class can be
    treated as a simple container object.
    """

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    @staticmethod
    def _checkatom(atom):
        if isinstance(atom, str):
            atom = getattr(elements, atom)
        elif not isinstance(atom, Atom):
            raise TypeError("atom must be an instance of class "
                            "xrayutilities.materials.Atom")
        return atom

    @staticmethod
    def _checkpos(pos):
        if isinstance(pos, str):
            pos = (pos, None)
        elif isinstance(pos, (tuple, list)):
            if isinstance(pos[1], numbers.Number):
                pos = (pos[0], (pos[1], ))
        return pos

    def append(self, atom, pos, occ=1.0, b=0.):
        """
        add new Atom to the lattice base

        Parameters
        ----------
         atom:   atom object to be added
         pos:    Wyckoff position of the atom, along with its parameters.
                 Examples: ('2i', (0.1, 0.2, 0.3)), or '1a'
         occ:    occupancy (default=1.0)
         b:      b-factor of the atom used as exp(-b*q**2/(4*pi)**2) to reduce
                 the intensity of this atom (only used in case of temp=0 in
                 StructureFactor and chi calculation)
        """
        atom = self._checkatom(atom)
        pos = self._checkpos(pos)
        list.append(self, (atom, pos, occ, b))

    def __setitem__(self, key, data):
        (atom, pos, occ, b) = data
        atom = self._checkatom(atom)
        pos = self._checkpos(pos)
        list.__setitem__(self, key, (atom, pos, float(occ), float(b)))

    def __str__(self):
        ostr = ''
        for i, (atom, p, occ, b) in enumerate(self):
            ostr += '%d: %s %s ' % (i, str(atom), p[0])
            if p[1] is not None:
                ostr += ' '.join(['%.4f' % v for v in p[1]])
            ostr += ' occ=%5.3f b=%5.3f\n' % (occ, b)
        return ostr


class SGLattice(object):
    """
    lattice object created from the space group number and corresponding unit
    cell parameters. atoms in the unit cell are specified by their Wyckoff
    position and their free parameters.

    this replaces the deprecated Lattice class
    """
    def __init__(self, sgrp, *args, **kwargs):
        """
        initialize class with space group number and atom list

        Parameters
        ----------
         sgrp:  Space group number (or string)
         *args: space group parameters. depending on the space group number
                this are 1 (cubic) to 6 (triclinic) parameters.
                cubic: a (lattice parameter).
                hexagonal: a, c.
                trigonal: a, c.
                tetragonal: a, c.
                orthorhombic: a, b, c.
                monoclinic: a, b, c, beta (in degree).
                triclinic: a, b, c, alpha, beta, gamma (in degree).
         **kwargs: optional parameters
            atoms: list of elements either as Element object or string with the
                   element name. If you specify atoms you have to also give the
                   same number of Wyckoff positions
            pos:   list of the atoms Wyckoff positions along with its
                   parameters. If a position has no free parameter the
                   parameters can be omitted. Example:
                   [('2i', (0.1, 0.2, 0.3)), '1a']
            occ:   site occupation for the atoms. This is optional and defaults
                   to 1 if not given.
            b:     b-factor of the atom used as exp(-b*q**2/(4*pi)**2) to
                   reduce the intensity of this atom (only used in case of
                   temp=0 in StructureFactor and chi calculation)
        """
        self.space_group = str(sgrp)
        self.space_group_nr = int(self.space_group.split(':')[0])
        try:
            self.space_group_suf = ':' + self.space_group.split(':')[1]
        except:
            self.space_group_suf = ''
        # set default space group suffix if none is given
        if (self.space_group_nr in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                    15] and self.space_group_suf == ''):
            self.space_group_suf = ':b'
        elif (self.space_group_nr in [48, 50, 59, 68, 70, 85, 86, 88, 125, 126,
                                      129, 130, 133, 134, 137, 138, 141, 142,
                                      201, 203, 222, 224, 227, 228] and
              self.space_group_suf == ''):
            self.space_group_suf = ':1'
        elif (self.space_group_nr in [146, 148, 155, 160, 161, 166, 167] and
              self.space_group_suf == ''):
            self.space_group_suf = ':H'

        self.name = sgrp_name[str(self.space_group_nr)] + self.space_group_suf
        self.crystal_system, nargs = sgrp_sym[self.space_group_nr]
        self.crystal_system += self.space_group_suf
        if len(args) != nargs:
            raise ValueError('XU: number of parameters (%d) does not match the'
                             ' crystal symmetry (%s:%d)'
                             % (len(args), self.crystal_system, nargs))
        self.free_parameters = OrderedDict()
        for a, par in zip(args, sgrp_params[self.crystal_system][0]):
            self.free_parameters[par] = a

        self._parameters = OrderedDict()
        for i, p in enumerate(('a', 'b', 'c', 'alpha', 'beta', 'gamma')):
            key = sgrp_params[self.crystal_system][1][i]
            if isinstance(key, str):
                self._parameters[p] = self.free_parameters[key]
            else:
                self._parameters[p] = sgrp_params[self.crystal_system][1][i]

        # set atom positions in the lattice base
        self._wbase = WyckoffBase()
        atoms = kwargs.get('atoms', None)
        wps = kwargs.get('pos', None)
        if atoms:
            occs = kwargs.get('occ', [1.0, ] * len(atoms))
            bs = kwargs.get('b', [0.0, ] * len(atoms))
            for at, wp, o, b in zip(atoms, wps, occs, bs):
                self._wbase.append(at, wp, o, b)
        self.nsites = len(self._wbase)

        # define lattice vectors
        self._ai = numpy.zeros((3, 3))
        self._bi = numpy.empty((3, 3))
        a, b, c, alpha, beta, gamma = self._parameters.values()
        rg = radians(gamma)
        self._paramhelp = [cos(radians(alpha)), cos(radians(beta)),
                           cos(rg), sin(rg), 0]
        self._setlat()

    def base(self):
        """
        generator of atomic position within the unit cell.
        """
        if len(self._wbase) == 0:
            return
        sgwp = wp[str(self.space_group)]
        for (atom, w, occ, b) in self._wbase:
            x, y, z = None, None, None
            parint, poslist = sgwp[w[0]]
            i = 0
            if parint & 1:
                x = w[1][i]
                i += 1
            if parint & 2:
                y = w[1][i]
                i += 1
            if parint & 4:
                z = w[1][i]
            for p in poslist:
                pos = eval(p, {'x': x, 'y': y, 'z': z})
                yield atom, pos, occ, b

    def _setlat(self):
        a, b, c, alpha, beta, gamma = self._parameters.values()
        ca, cb, cg, sg, vh = self._paramhelp
        vh = sqrt(1 - ca**2-cb**2-cg**2 + 2*ca*cb*cg)
        self._paramhelp[4] = vh
        self._ai[0, 0] = a
        self._ai[1, 0] = b * cg
        self._ai[1, 1] = b * sg
        self._ai[2, 0] = c * cb
        self._ai[2, 1] = c * (ca-cb*cg) / sg
        self._ai[2, 2] = c * vh / sg
        self.transform = math.Transform(self._ai.T)
        self._setb()

    def _setb(self):
        V = self.UnitCellVolume()
        p = 2. * numpy.pi / V
        math.VecCross(p*self._ai[1, :], self._ai[2, :], out=self._bi[0, :])
        math.VecCross(p*self._ai[2, :], self._ai[0, :], out=self._bi[1, :])
        math.VecCross(p*self._ai[0, :], self._ai[1, :], out=self._bi[2, :])
        self.qtransform = math.Transform(self._bi.T)

    def _set_params_from_sym(self):
        for i, p in enumerate(('a', 'b', 'c', 'alpha', 'beta', 'gamma')):
            key = sgrp_params[self.crystal_system][1][i]
            if isinstance(key, str):
                self._parameters[p] = self.free_parameters[key]

    @property
    def a(self):
        return self._parameters['a']

    @a.setter
    def a(self, value):
        if 'a' not in self.free_parameters:
            raise RuntimeError("a can not be set, its not a free parameter!")
        self._parameters['a'] = value
        self.free_parameters['a'] = value
        self._set_params_from_sym()
        self._setlat()

    @property
    def b(self):
        return self._parameters['b']

    @b.setter
    def b(self, value):
        if 'b' not in self.free_parameters:
            raise RuntimeError("b can not be set, its not a free parameter!")
        self._parameters['b'] = value
        self.free_parameters['b'] = value
        self._set_params_from_sym()
        self._setlat()

    @property
    def c(self):
        return self._parameters['c']

    @c.setter
    def c(self, value):
        if 'c' not in self.free_parameters:
            raise RuntimeError("c can not be set, its not a free parameter!")
        self._parameters['c'] = value
        self.free_parameters['c'] = value
        self._set_params_from_sym()
        self._setlat()

    @property
    def alpha(self):
        return self._parameters['alpha']

    @alpha.setter
    def alpha(self, value):
        if 'alpha' not in self.free_parameters:
            raise RuntimeError("alpha can not be set for this space group!")
        self._parameters['alpha'] = value
        self.free_parameters['alpha'] = value
        self._set_params_from_sym()
        self._paramhelp[0] = cos(radians(value))
        self._setlat()

    @property
    def beta(self):
        return self._parameters['beta']

    @beta.setter
    def beta(self, value):
        if 'beta' not in self.free_parameters:
            raise RuntimeError("beta can not be set for this space group!")
        self._parameters['beta'] = value
        self.free_parameters['beta'] = value
        self._set_params_from_sym()
        self._paramhelp[1] = cos(radians(value))
        self._setlat()

    @property
    def gamma(self):
        return self._parameters['gamma']

    @gamma.setter
    def gamma(self, value):
        if 'gamma' not in self.free_parameters:
            raise RuntimeError("gamma can not be set for this space group!")
        self._parameters['gamma'] = value
        self.free_parameters['gamma'] = value
        self._set_params_from_sym()
        rg = radians(value)
        self._paramhelp[2] = cos(rg)
        self._paramhelp[3] = sin(rg)
        self._setlat()

    def GetPoint(self, *args):
        """
        determine lattice points with indices given in the argument

        Examples
        --------
        >>> xu.materials.Si.lattice.GetPoint(0,0,4)
        array([  0.     ,   0.     ,  21.72416])

        or

        >>> xu.materials.Si.lattice.GetPoint((1,1,1))
        array([ 5.43104,  5.43104,  5.43104])
        """
        if len(args) == 1:
            args = args[0]
        return self.transform(args)

    def GetQ(self, *args):
        """
        determine the reciprocal lattice points with indices given in the
        argument
        """
        if len(args) == 1:
            args = args[0]
        return self.qtransform(args)

    def UnitCellVolume(self):
        """
        function to calculate the unit cell volume of a lattice (angstrom^3)
        """
        a, b, c, alpha, beta, gamma = self._parameters.values()
        return a * b * c * self._paramhelp[4]

    def ApplyStrain(self, eps):
        """
        Applies a certain strain on a lattice. The result is a change
        in the base vectors. The full strain matrix (3x3) needs to be given.
        Note: Here you specify the strain and not the stress -> NO elastic
              response of the material will be considered!

        Parameters
        ----------
         eps:    a 3x3 matrix with all strain components
        """
        if isinstance(eps, (list, tuple)):
            eps = numpy.asarray(eps, dtype=numpy.double)
        if eps.shape != (3, 3):
            raise InputError("ApplyStrain needs a 3x3 matrix "
                             "with strain values")

        ai = self._ai + numpy.dot(eps, self._ai.T).T
        self._parameters['a'] = math.VecNorm(ai[0, :])
        self._parameters['b'] = math.VecNorm(ai[1, :])
        self._parameters['c'] = math.VecNorm(ai[2, :])
        self._parameters['alpha'] = math.VecAngle(ai[1, :], ai[2, :], deg=True)
        self._parameters['beta'] = math.VecAngle(ai[0, :], ai[2, :], deg=True)
        self._parameters['gamma'] = math.VecAngle(ai[0, :], ai[1, :], deg=True)
        # update helper parameters
        self._paramhelp[0] = cos(radians(self._parameters['alpha']))
        self._paramhelp[1] = cos(radians(self._parameters['beta']))
        rg = radians(self._parameters['gamma'])
        self._paramhelp[2] = cos(rg)
        self._paramhelp[3] = sin(rg)
        # set new transformations
        self._setlat()

    def isequivalent(self, hkl1, hkl2, equalq=False):
        """
        primitive way of determining if hkl1 and hkl2 are two
        crystallographical equivalent pairs of Miller indices

        Parameters
        ----------
         hkl1,2:        Miller indices to be checked for equivalence
         equalq:        If False the length of the two q-vactors will be
                        compared. If True it is assumed that the length of the
                        q-vectors of hkl1 and hkl2 is equal!

        Returns
        -------
         True or False
        """
        def leftShift(tup, n):
            try:
                n = n % len(tup)
            except ZeroDivisionError:
                return tuple()
            return tup[n:] + tup[0:n]

        def ispermutation(t1, t2):
            """returns true if t2 is an even permutation of t1"""
            if t1 == t2 or t1 == leftShift(t2, 1) or t1 == leftShift(t2, 2):
                return True
            else:
                return False

        def checkequal(hkl1, hkl2):
            if self.crystal_system.startswith('cubic'):
                if self.space_group_nr < 207:
                    if ispermutation(tuple(numpy.abs(hkl1)),
                                     tuple(numpy.abs(hkl2))):
                        return True
                    else:
                        return False
                else:
                    khl1 = (hkl1[1], hkl1[0], hkl1[2])
                    if (ispermutation(tuple(numpy.abs(hkl1)),
                                      tuple(numpy.abs(hkl2))) or
                        ispermutation(tuple(numpy.abs(khl1)),
                                      tuple(numpy.abs(hkl2)))):
                        return True
                    else:
                        return False
            elif self.crystal_system.startswith('hexagonal'):
                hki1 = (hkl1[0], hkl1[1], -hkl1[0] - hkl1[1])
                hki2 = (hkl2[0], hkl2[1], -hkl2[0] - hkl2[1])
                if (abs(hkl1[2]) == abs(hkl2[2]) and
                        sum(numpy.abs(hki1)) == sum(numpy.abs(hki2))):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('trigonal:R'):
                khl1 = (hkl1[1], hkl1[0], hkl1[2])
                if (ispermutation(hkl1, hkl2) or ispermutation(khl1, hkl2)):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('trigonal'):
                hki1 = (hkl1[0], hkl1[1], -hkl1[0] - hkl1[1])
                hki2 = (hkl2[0], hkl2[1], -hkl2[0] - hkl2[1])
                khi2 = (hkl2[1], hkl2[0], -hkl2[0] - hkl2[1])
                if ((hkl1[2] == hkl2[2] and ispermutation(hki1, hki2)) or
                        (hkl1[2] == -hkl2[2] and ispermutation(hki1, khi2))):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('tetragonal'):
                # this neglects that in some tetragonal materials hkl = khl
                hk1 = hkl1[:2]
                hk2 = hkl2[:2]
                if (abs(hkl1[2]) == abs(hkl2[2]) and
                        (hk1 == hk2 or hk1 == (-hk2[1], hk2[0]) or
                         hk1 == (-hk2[0], -hk2[1]) or
                         hk1 == (hk2[1], -hk2[0]))):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('orthorhombic'):
                if numpy.all(numpy.abs(hkl1) == numpy.abs(hkl2)):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('monoclinic:c'):
                hk1 = (hkl1[0], hkl1[1])
                hk2 = (hkl2[0], hkl2[1])
                if (abs(hkl1[2]) == abs(hkl2[2]) and
                        (hk1 == hk2 or hk1 == (-hk2[0], -hk2[1]))):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('monoclinic'):
                hl1 = (hkl1[0], hkl1[2])
                hl2 = (hkl2[0], hkl2[2])
                if (abs(hkl1[1]) == abs(hkl2[1]) and
                        (hl1 == hl2 or hl1 == (-hl2[0], -hl2[1]))):
                    return True
                else:
                    return False
            elif self.crystal_system.startswith('triclinic'):
                if (hkl1[0] == -hkl2[0] and hkl1[1] == -hkl2[1] and
                        hkl1[2] == -hkl2[2]):
                    return True
                else:
                    return False

        if equalq:
            return checkequal(tuple(hkl1), tuple(hkl2))
        else:
            if math.VecNorm(self.getQ(hkl1)) != math.VecNorm(self.getQ(hkl2)):
                return False
            else:
                return checkequal(tuple(hkl1), tuple(hkl2))

    def __str__(self):
        ostr = "{sg} {cs} {n}: a = {a:.4f}, b = {b:.4f} c= {c:.4f}\n" +\
               "alpha = {alpha:.3f}, beta = {beta:.3f}, gamma = {gamma:.3f}\n"
        ostr = ostr.format(sg=self.space_group, cs=self.crystal_system,
                           n=self.name, **self._parameters)
        if len(self._wbase) > 0:
            ostr += "Lattice base:\n"
            ostr += str(self._wbase)
        return ostr

    def __copy__(self):
        """
        return a copy of this SGLattice instance
        """
        atoms = []
        pos = []
        occ = []
        biso = []
        for at, wp, o, b in self._wbase:
            atoms.append(at)
            pos.append(wp)
            occ.append(o)
            biso.append(b)
        return SGLattice(self.space_group, *self.free_parameters.values(),
                         atoms=atoms, pos=pos, occ=occ, b=biso)

    @classmethod
    def fromLattice(cls, lat, verbose=True):
        """
        create a SGLattice from an old Lattice instance. Since the
        space-group is not known it will always be 1 (triclinic). This is
        helper routine to make the transition period for users easier. It will
        be removed in the next major release!

        Parameters
        ----------
         lat:   deprecated Lattice instance

        Returns
        -------
        SGLattice instance with the same properties as lat
        """
        a, b, c, alpha, beta, gamma = (lat.a, lat.b, lat.c, lat.alpha,
                                       lat.beta, lat.gamma)
        atoms = []
        pos = []
        occ = []
        biso = []
        for at, p, o, bf in lat.base:
            atoms.append(at)
            pos.append(('1a', p))
            occ.append(o)
            biso.append(bf)
        if verbose:
            print('xu.materials.SGLattice(1, %f, %f, %f, %f, %f, %f, '
                  'atoms=%s, pos=%s, occ=%s, b=%s)'
                  % (a, b, c, alpha, beta, gamma, str(atoms), str(pos),
                     str(occ), str(biso)))
        return cls(1, a, b, c, alpha, beta, gamma, atoms=atoms, pos=pos,
                   occ=occ, b=biso)

    @classmethod
    def convert_to_P1(cls, sglat):
        """
        create a P1 equivalent of the given SGLattice instance.

        Parameters
        ----------
         sglat:   space group lattice instance to be converted to P1.

        Returns
        -------
        SGLattice instance with the same properties as sglat, however in the P1
        setting.
        """
        a, b, c, alpha, beta, gamma = (sglat.a, sglat.b, sglat.c, sglat.alpha,
                                       sglat.beta, sglat.gamma)
        atoms = []
        pos = []
        occ = []
        biso = []
        for at, p, o, bf in sglat.base():
            atoms.append(at)
            pos.append(('1a', p))
            occ.append(o)
            biso.append(bf)
        return cls(1, a, b, c, alpha, beta, gamma, atoms=atoms, pos=pos,
                   occ=occ, b=biso)
