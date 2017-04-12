"""
This file is part of Havaiana.

    Havaiana is free software: you can redistribute it and/or modify
    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Havaiana is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU  Lesser General Public License
    along with Havaiana.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import

from .__init__ import Site

import ojota.examples.examples as pkg

if __name__ == '__main__':
    site = Site(pkg)
    site.serve()
