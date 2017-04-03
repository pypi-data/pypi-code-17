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
# Copyright (C) 2012-2017 Dominik Kriegner <dominik.kriegner@gmail.com>

import xrayutilities as xu
import numpy

# definition of materials is done from its space group and its free parameters.
# Atoms in the base are specified by their Wyckoff positions and potential free
# parameters of these positions

# As example we will refine zinc-blende InP which is already predefined as
# xu.materials.InP. Zincblende consists of atoms

# elements (which contain their x-ray optical properties) are loaded from
# xrayutilities.materials.elements
In = xu.materials.elements.In
P = xu.materials.elements.P

# definition of zincblende InP:
InP = xu.materials.Crystal(
    "InP", xu.materials.SGLattice(216, 5.8687, atoms=[In, P],
                                  pos=['4a', '4c']),)

# printing of information about the defined material:
print(InP)

# for some purposes it might be necessary to convert the SGLattice to space
# group P1
InP_p1 = xu.materials.Crystal(
    "InP (P1)", xu.materials.SGLattice.convert_to_P1(InP.lattice))

print(InP_p1)
