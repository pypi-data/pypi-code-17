import pygame


# ################################################ GAME WALL OBJECT ####################################################
class Wall(pygame.sprite.Sprite):
    def __init__(self, world, x, y, w, h, group):
        self.world = world
        self.groups = group     # Should be PyManMain.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect.x = x
        self.rect.y = y