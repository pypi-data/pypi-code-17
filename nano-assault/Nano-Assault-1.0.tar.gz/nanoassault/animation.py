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

import os

from .constants import SCALEFAC

import pygame

class Animation(object):
    def __init__(self, frame_names, speed):
        self.frame_names = frame_names
        self.frames = [pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "%s.png" % f)) for f in self.frame_names]
        self.frames = [pygame.transform.scale(f, (f.get_width()*SCALEFAC, f.get_height()*SCALEFAC)) for f in self.frames]
        self.frame = 0
        self.frame_timer = 0
        self.speed = speed

    def tick(self, factor=1):
        self.frame_timer += factor
        if self.frame_timer >= self.speed:
            self.frame_timer = 0
            self.frame += 1
            if self.frame == len(self.frames):
                self.frame = 0
        return self.frames[self.frame]
