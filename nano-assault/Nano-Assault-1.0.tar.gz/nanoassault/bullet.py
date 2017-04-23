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
from .animation import Animation

class Bullet(Actor):
    def __init__(self, image, pos, motion, timer, damage):
        Actor.__init__(self, (Animation((image,), 0),), pos)
        self.rect.center = pos

        self.motion = motion
        self.speed = self.speed_fast
        self.timer = timer
        self.damage = damage

        self.byplayer = False

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
            return
        self.move()
        self.update_image()
