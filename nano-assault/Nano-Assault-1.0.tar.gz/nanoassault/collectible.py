# ~*~ coding: utf-8 ~*~

# (C) 2017, Eike Jesinghaus
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .animation import Animation
from .constants import SCALEFAC
from .gameobject import GameObject

class Collectible(GameObject):
    def __init__(self, image, pos):
        GameObject.__init__(self, (Animation((image,), 0),), (pos[0]*16*SCALEFAC, pos[1]*16*SCALEFAC))

    def on_collect(self, player):
        pass
