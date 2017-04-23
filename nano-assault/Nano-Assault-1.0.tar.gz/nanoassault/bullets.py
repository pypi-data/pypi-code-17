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

from .bullet import Bullet

class BulletPlayer(Bullet):
    def __init__(self, pos, motion):
        Bullet.__init__(self, "bullet_player0", pos, motion, 60, 3)
        self.speed = self.speed_fast
        self.byplayer = True

class BulletEnemy0(Bullet):
    def __init__(self, pos, motion):
        Bullet.__init__(self, "bullet_enemy0", pos, motion, 60, 1)
        self.speed = self.speed_norm

class BulletEnemy1(BulletEnemy0):
    def __init__(self, pos, motion):
        BulletEnemy0.__init__(self, pos, motion)
        self.speed = self.speed_fast