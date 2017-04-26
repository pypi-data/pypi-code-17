#
# This file is part of SpectralToolbox.
#
# SpectralToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpectralToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with SpectralToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Daniele Bigoni
#

from numpy.distutils.core import setup
from numpy.distutils.core import Extension
import os
import glob
        
ext_modules = [ Extension('orthpol_light',
                          glob.glob(os.path.join('src','*.f'))) ]

setup(
    name='orthpol_light',
    version = "1.0.1",
    license = "COPYING.LESSER",
    description = "Light python wrapper for the ORTHPOL package",
    long_description=open("README.rst").read(),
    url="http://www.limitcycle.it",
    author = "Daniele Bigoni",
    author_email = "dabi@limitcycle.it",
    ext_modules = ext_modules
)

