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

from .constants import SCALEFAC, TILEX, TILEY
from .player import Player
from .dungeon import Dungeon
from .run_dungeon import run_dungeon
from .levels import ALL_LEVELS, BOSS_LEVELS

import pygame

def main():
    screen = pygame.display.set_mode((TILEX*16*SCALEFAC, TILEY*16*SCALEFAC+8*SCALEFAC), pygame.FULLSCREEN)
    pygame.display.set_caption("Nano Assault")

    for i in ("titlescreen", "intro"):
        titlescreen = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "%s.png" % i))
        titlescreen = pygame.transform.scale(titlescreen, screen.get_size())
        screen.blit(titlescreen, (0, 0))
        pygame.display.update()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                else:
                    break

    player = Player((screen.get_width()/2-SCALEFAC*8, screen.get_height()/2-SCALEFAC*12))

    dungeon = Dungeon("fleshy", 12)
    dungeon.generate(ALL_LEVELS, BOSS_LEVELS)

    run_dungeon(screen, dungeon, player)

    return 0
