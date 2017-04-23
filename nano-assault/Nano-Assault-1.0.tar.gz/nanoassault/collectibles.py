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

from .collectible import Collectible

class Energy(Collectible):
    def __init__(self, pos):
        Collectible.__init__(self, "collectible_energy", pos)

    def on_collect(self, player):
        player.hp += 1

class Spasmolytic(Collectible):
    def __init__(self, pos):
        Collectible.__init__(self, "collectible_spasmolytic", pos)

    def on_collect(self, player):
        player.keys += 1
