import pygame
import abc as _abc


# Class represent wall game objects
class WallI(object):
    __metaclass__ = _abc.ABCMeta


# Class represent item game objects
class Item(object):
    __metaclass__ = _abc.ABCMeta


# Class represent item actor game objects
class IActor(object):
    __metaclass__ = _abc.ABCMeta


# Class represent player game objects
class Player(object):
    __metaclass__ = _abc.ABCMeta


# Class represent game objects to put in game
class Actor(pygame.sprite.Sprite):
    __metaclass__ = _abc.ABCMeta

    @_abc.abstractmethod
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self._sprite = None
        self.rect = None
        self.world = None

    @_abc.abstractmethod
    def update(self):
        pass

    def get_groups(self):
        return self.groups()

    def set_group(self, group):
        self.add(group)

    def set_world(self, world):
        self.world = world

    def set_animation(self, spritesheet):
        self._sprite = spritesheet
        self.rect = spritesheet.image.get_rect()

    def get_image(self):
        return self._sprite

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    def get_intersecting_actors(self):
        intersectingList = []
        x = self.x
        y = self.y
        w = self.rect.width
        h = self.rect.height

        for list in self.world.worldList:
            for sprite in list:
                sx = sprite.rect.x
                sy = sprite.rect.y
                sw = sprite.rect.width
                sh = sprite.rect.height
                if (not((x >= sx + sw) or (x + w <= sx) or (y >= sy + sh) or (y + h <= sy))):
                    intersectingList.append(sprite)
        return intersectingList

    def intersectsWithWall(self, dx, dy):
        x = self.x + dx
        y = self.y - dy
        w = self.rect.width
        h = self.rect.height

        for wall in self.world.walls:
            if ((x >= wall.x + wall.width) or
                    (x + w <= wall.x) or
                    (y >= wall.y + wall.height) or
                    (y + h <= wall.y)):
                continue
            else:
                return True


# Class represent game objects that write to screen
class WriteToDisplay(object):
    __metaclass__ = _abc.ABCMeta

    @_abc.abstractmethod
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 15)
        self.color = (255, 255, 255)

    def setFont(self, font, size):
        self.font = pygame.font.SysFont(font, size)

    def write(self, infotext, dest, world, antialias=1):
        info = self.font.render(infotext, antialias, self.color)
        world.screen.blit(info, dest)


# Pull individual sprites from sprite sheets
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, gameObject, file_name, sw, sh, frames):
        """ Constructor. Pass in the file name of the sprite sheet. """
        self.gameObject = gameObject
        self.black = (0, 0, 0)

        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        self.images = self.get_all_images(self.sprite_sheet.get_rect().width,
                                          self.sprite_sheet.get_rect().height,
                                          sw, sh, frames)
        self.image = self.images[0]
        self.gameObject.image = self.image
        self.pingpong = True
        # self.iterator = iter(self.images)

        self.fps = 60
        self.anim_speed = 3
        self.play_frame = round(self.fps / (frames * self.anim_speed))
        self.anim_frames = frames - 1
        self.current_frame = 1
        self.current_anim_frame = 0
        self.plus = True

    def play(self):
        if(self.anim_frames > 0):
            if(self.current_frame == self.play_frame):
                if(self.pingpong is False):
                    if(self.current_anim_frame < self.anim_frames):
                        self.current_anim_frame += 1
                    else:
                        self.current_anim_frame = 0
                else:
                    if(self.plus is True and self.current_anim_frame < self.anim_frames):
                        self.current_anim_frame += 1
                        if(self.current_anim_frame == self.anim_frames):
                            self.plus = False
                    elif(self.plus is False and self.current_anim_frame > 0):
                        self.current_anim_frame -= 1
                        if (self.current_anim_frame == 0):
                            self.plus = True
            self.gameObject.image = self.images[self.current_anim_frame]

            if(self.current_frame < self.play_frame):
                self.current_frame += 1
            else:
                self.current_frame = 1

    def stop(self):
        pass

    def get_all_images(self, fwidth, fheight, swidth, sheight, frames):
        """ Return single images from larger spritesheet in list.
            fwidth/fheight is full with and height of the picture,
            swidth/sheight is single sprite width and height of
            the picture. Frames is number of frames in spritesheet"""
        images = []
        total = 0
        for i in range(0, fheight, sheight):
            for y in range(0, fwidth, swidth):
                images.append(self.get_image(y, i, swidth, sheight))
                total += 1
                if (total >= frames):
                    break
        return images

    def get_image(self, x, y, iwidth, iheight):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([iwidth, iheight]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, iwidth, iheight))

        # Assuming black works as the transparent color
        image.set_colorkey(self.black)

        # Return the image
        return image


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
        self.image = pygame.Surface([self.width, self.height])
        color = 255, 255, 255, 255
        self.image.set_colorkey(color)
        self.image.fill(color)
