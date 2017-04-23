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

from .constants import SCALEFAC, TILEX, TILEY
from .wall import Wall

import os

import pygame

class Level(object):
    def __init__(self, theme, walls, enemies, keylevel, contains=None):
        self.theme = theme
        self.walls = list(walls)
        self.enemies = enemies

        self.keylevel = keylevel
        self.parent = None
        self.children = []

        self.up = None
        self.down = None
        self.left = None
        self.right = None

        self.cleared = False
        self.unlocked = False

        self.contains = contains

        self.label = "O"

        self.keypos = (7.5, 5.5)

    def generate_walls(self):
        walls = [("topleft", (0, 0)), ("topright", (16*(TILEX-1)*SCALEFAC, 0)), ("bottomleft", (0, 16*(TILEY-1)*SCALEFAC)), ("bottomright", (16*(TILEX-1)*SCALEFAC, 16*(TILEY-1)*SCALEFAC))] + self.walls

        for i in range(1, TILEX-1):
            if not (i in (TILEX/2, TILEX/2-1) and self.up):
                walls += [("top", (16*i*SCALEFAC, 0))]
            if not (i in (TILEX/2, TILEX/2-1) and self.down):
                walls += [("bottom", (16*i*SCALEFAC, 16*(TILEY-1)*SCALEFAC))]

        for i in range(1, TILEY-1):
            if not (i in (TILEY/2, TILEY/2-1) and self.left):
                walls += [("left", (0, 16*i*SCALEFAC))]
            if not (i in (TILEY/2, TILEY/2-1) and self.right):
                walls += [("right", (16*(TILEX-1)*SCALEFAC, 16*i*SCALEFAC))]

        walls = [Wall("level_%s_%s" % (self.theme, w[0]), w[1]) for w in walls]

        return walls

    def generate_enemies(self):
        return [e[0]((e[1][0]*16*SCALEFAC, e[1][1]*16*SCALEFAC), *e[2:]) for e in self.enemies] if not self.cleared else []

    def generate_bg(self):
        bg = pygame.Surface((16*TILEX*SCALEFAC, 16*TILEY*SCALEFAC))

        bgimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "level_%s_ground.png" % self.theme))
        bgimg = pygame.transform.scale(bgimg, (bgimg.get_width()*SCALEFAC, bgimg.get_height()*SCALEFAC))

        upimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "level_%s_topdoor0.png" % self.theme))
        downimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "level_%s_bottomdoor0.png" % self.theme))
        leftimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "level_%s_leftdoor0.png" % self.theme))
        rightimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "level_%s_rightdoor0.png" % self.theme))

        upimg = pygame.transform.scale(upimg, (upimg.get_width()*SCALEFAC, upimg.get_height()*SCALEFAC))
        downimg = pygame.transform.scale(downimg, (downimg.get_width()*SCALEFAC, downimg.get_height()*SCALEFAC))
        leftimg = pygame.transform.scale(leftimg, (leftimg.get_width()*SCALEFAC, leftimg.get_height()*SCALEFAC))
        rightimg = pygame.transform.scale(rightimg, (rightimg.get_width()*SCALEFAC, rightimg.get_height()*SCALEFAC))

        for y in range(0, TILEY):
            for x in range(0, TILEX):
                bg.blit(bgimg, (16*x*SCALEFAC, 16*y*SCALEFAC))

        if self.up:
            bg.blit(upimg, (16*SCALEFAC*(TILEX/2-1), 0))
        if self.down:
            bg.blit(downimg, (16*SCALEFAC*(TILEX/2-1), 16*SCALEFAC*(TILEY-1)))
        if self.left:
            bg.blit(leftimg, (0, 16*SCALEFAC*(TILEY/2-1)))
        if self.right:
            bg.blit(rightimg, (16*SCALEFAC*(TILEX-1), 16*SCALEFAC*(TILEY/2-1)))

        return bg

    def generate_doors(self):
        doors = []
        if self.up:
            if self.up[1] and not self.unlocked:
                doors.append(Wall("level_%s_toplocked0" % self.theme, (16*SCALEFAC*(TILEX/2-1), 0), 1))
            elif not self.cleared:
                doors.append(Wall("level_%s_topclosed0" % self.theme, (16*SCALEFAC*(TILEX/2-1), 0), 2))
        if self.down:
            if self.down[1] and not self.unlocked:
                doors.append(Wall("level_%s_bottomlocked0" % self.theme, (16*SCALEFAC*(TILEX/2-1), 16*SCALEFAC*(TILEY-1)), 1))
            elif not self.cleared:
                doors.append(Wall("level_%s_bottomclosed0" % self.theme, (16*SCALEFAC*(TILEX/2-1), 16*SCALEFAC*(TILEY-1)), 2))
        if self.left:
            if self.left[1] and not self.unlocked:
                doors.append(Wall("level_%s_leftlocked0" % self.theme, (0, 16*SCALEFAC*(TILEY/2-1)), 1))
            elif not self.cleared:
                doors.append(Wall("level_%s_leftclosed0" % self.theme, (0, 16*SCALEFAC*(TILEY/2-1)), 2))
        if self.right:
            if self.right[1] and not self.unlocked:
                doors.append(Wall("level_%s_rightlocked0" % self.theme, (16*SCALEFAC*(TILEX-1), 16*SCALEFAC*(TILEY/2-1)), 1))
            elif not self.cleared:
                doors.append(Wall("level_%s_rightclosed0" % self.theme, (16*SCALEFAC*(TILEX-1), 16*SCALEFAC*(TILEY/2-1)), 2))
        return doors


    def clear(self, collectibles, doors):
        self.cleared = True
        if self.contains:
            collectibles.add(self.contains)
        for d in doors:
            if d.door == 2:
                d.kill()
