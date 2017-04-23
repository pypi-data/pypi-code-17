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

from random import randint

from .animations import animations_enemy_coccusdesertus, animations_enemy_coccusiactans, animations_boss_coccusimmanis, animations_enemy_bacillusceler
from .bullets import BulletEnemy0, BulletEnemy1
from .enemy import Enemy

class CoccusDesertus(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, "Coccus desertus", animations_enemy_coccusdesertus, pos, 5, 1)
        self.still_counter = 60
        self.speed = self.speed_norm

    def coll_obstacle(self, obstacle):
        Enemy.coll_obstacle(self, obstacle)
        self.still_counter = 1

    def update(self, player, bullets):
        if self.isdead():
            self.kill()
            return

        self.still_counter -= 1
        if self.still_counter == 0:
            self.motion = ((0, -1), (0, 1), (-1, 0), (1, 0))[randint(0, 3)]
            self.change_anim(0)
        elif self.still_counter == -80:
            self.motion = (0, 0)
            self.still_counter = 30
            self.change_anim(1)

        self.move()
        self.update_image()

class CoccusIactans(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, "Coccus iactans", animations_enemy_coccusiactans, pos, 8, 1)
        self.still_counter = 60

    def coll_obstacle(self, obstacle):
        Enemy.coll_obstacle(self, obstacle)
        self.still_counter = 1

    def update(self, player, bullets):
        if self.isdead():
            self.kill()
            return

        self.still_counter -= 1
        if self.still_counter == 0:
            self.motion = ((-1, -1), (1, 1), (-1, 1), (1, -1))[randint(0, 3)]
            self.change_anim(0)
        elif self.still_counter == -80:
            self.motion = (0, 0)
            self.still_counter = 60
            self.change_anim(1)
            bullets.add(BulletEnemy1(self.rect.center, (0, 1)))
            bullets.add(BulletEnemy1(self.rect.center, (0, -1)))
            bullets.add(BulletEnemy1(self.rect.center, (1, 0)))
            bullets.add(BulletEnemy1(self.rect.center, (-1, 0)))


        self.move()
        self.update_image()

class CoccusImmanis(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, "Coccus immanis", animations_boss_coccusimmanis, pos, 26, 1)
        self.speed = self.speed_fast
        self.rotation_timer = 40
        self.rot = 0
        self.shot_timer = 0

    def coll_obtacle(self, obstacle):
        Enemy.coll_obstacle(self, obstacle)
        self.motion = ((-1, 0), (1, 0), (0, -1), (0, 1))[randint(0, 1)+2*self.rot]

    def update(self, player, bullets):
        if self.isdead():
            self.kill()
            return

        self.rotation_timer -= 1
        if self.rotation_timer == 0:
            self.rot = (self.rot+1)%2
            self.change_anim(self.rot)
            self.rotation_timer = 40
            self.shot_timer = 15
            self.motion = ((-1, 0), (1, 0), (0, -1), (0, 1))[randint(0, 1)+2*self.rot]

        if self.shot_timer:
            self.shot_timer -= 1
            if self.shot_timer % 5 == 0:
                if self.rot == 0:
                    bullets.add(BulletEnemy1(self.rect.center, (0, 1)))
                    bullets.add(BulletEnemy1(self.rect.center, (0, -1)))
                elif self.rot == 1:
                    bullets.add(BulletEnemy1(self.rect.center, (1, 0)))
                    bullets.add(BulletEnemy1(self.rect.center, (-1, 0)))
                

        self.move()
        self.update_image()

class BacillusCeler(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, "Bacillus celer", animations_enemy_bacillusceler, pos, 3, 1)
        self.speed = self.speed_megafast
        self.dtimer = 40

    def coll_obstacle(self, obstacle):
        Enemy.coll_obstacle(self, obstacle)
        self.motion = ((0, 1), (0, -1), (1, 0), (-1, 0))[randint(0, 3)]

    def update(self, player, bullets):
        if self.isdead():
            self.kill()
            return

        self.dtimer -= 1
        if self.dtimer == 0:
            self.dtimer = 40
            self.motion = ((0, 1), (0, -1), (1, 0), (-1, 0))[randint(0, 3)]

        if self.motion[1] == 0:
            self.change_anim(1)
        else:
            self.change_anim(0)

        self.move()
        self.update_image()
