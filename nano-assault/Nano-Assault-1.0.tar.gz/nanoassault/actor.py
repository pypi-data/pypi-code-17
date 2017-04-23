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

from .constants import SPEED_SLOW, SPEED_NORM, SPEED_FAST, SPEED_MEGAFAST
from .gameobject import GameObject

class Actor(GameObject):
    def __init__(self, p_animations, pos):
        GameObject.__init__(self, p_animations, pos)

        self.motion = [0, 0]
        self.knockback = [0, 0]
        self.oldpos = self.rect.topleft

        self.speed_slow = SPEED_SLOW
        self.speed_norm = SPEED_NORM
        self.speed_fast = SPEED_FAST
        self.speed_megafast = SPEED_MEGAFAST

        self.speed = self.speed_norm

        self.knockback_timer = 0
        self.invincibility_frames = 0

    def hit(self, target):
        if target.invincibility_frames > 0:
            return
        target.get_damage(self.damage)
        if not (self.motion[0] == 0 and self.motion[1] == 0):
            kb = self.motion
        else:
            kb = [-1*i for i in target.motion]
        target.get_knockback(kb)

    def get_damage(self, damage):
        self.hp -= damage

    def get_knockback(self, motion):
        self.knockback = motion
        self.knockback_timer = 8

    def move(self):
        self.oldpos = self.rect.topleft
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.rect.move_ip(self.knockback[0]*self.speed_megafast, self.knockback[1]*self.speed_megafast)
        else:
            self.rect.move_ip(self.motion[0]*self.speed, self.motion[1]*self.speed)

    def coll_obstacle(self, obstacle):
        self.rect.topleft = self.oldpos

    def update(self):
        self.invincibility_frames -= 1 if self.invincibility_frames > 0 else 0
