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

import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, p_animations, pos):
        pygame.sprite.Sprite.__init__(self)
        self.animations = p_animations
        self.anim_index = 0
        self.animation = self.animations[self.anim_index]
        self.image = self.animation.tick(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        pass

    def change_anim(self, anim_index):
        if self.anim_index == anim_index:
            return
        self.anim_index = anim_index
        self.animation = self.animations[self.anim_index]

    def update_image(self):
        self.image = self.animation.tick()
