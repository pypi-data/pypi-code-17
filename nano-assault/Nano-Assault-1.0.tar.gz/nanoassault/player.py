# ~*~ coding: utf-8 ~*~

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
from .animations import animations_player

class Player(Actor):
    def __init__(self, pos):
        Actor.__init__(self, animations_player, pos)

        self.hp = 5

        self.keys = 0

        self.bullet_cooldown = 0

    def isdead(self):
        return self.hp <= 0

    def get_damage(self, damage):
        self.invincibility_frames = 60
        Actor.get_damage(self, damage)

    def update(self):
        if self.isdead():
            return False
        if self.bullet_cooldown:
            self.bullet_cooldown -= 1
        self.move()
        self.update_image()
        Actor.update(self)
        return True
