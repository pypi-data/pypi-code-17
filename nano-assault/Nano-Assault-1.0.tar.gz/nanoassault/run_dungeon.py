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

from .run_level import run_level

import os

import pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

def run_dungeon(screen, dungeon, player):
    next_level = dungeon.rooms[5][5]

    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sound", "theme0.wav"))
    pygame.mixer.music.play(-1)

    while True:
        next_level = run_level(screen, next_level, player)
        if next_level.label == "B":
            pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sound", "theme1.wav"))
            pygame.mixer.music.play(-1)
