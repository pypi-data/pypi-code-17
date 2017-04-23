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

from .actor import Actor

class Enemy(Actor):
    def __init__(self, name, animations, pos, hp, contact_damage):
        Actor.__init__(self, animations(), pos)
        self.name = name

        self.hp = hp
        self.damage = contact_damage

    def isdead(self):
        return self.hp <= 0

    def contact(self, player):
        self.hit(player)

    def update(self, player, bullets):
        pass
