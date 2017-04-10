import sys as _sys
import abc as _abc
import time as _time
import atexit as _atexit
import pygame
from importlib import reload as _reload
from watchdog.observers import Observer as _Observer
from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler


# ##############################################  EXCEPTIONS  ##########################################################
# Exception raised by pgc module
class _PGCException(Exception):
    pass


# Decorator for checking if game exists
def _game_exists(original_function):
    def wrapper_function(*args, **kwargs):
        if(game._game_thread is None or not game._game_thread.is_alive()):
            raise _PGCException('Game is not running. You have to start a game first.')
        else:
            return original_function(*args, **kwargs)
    return wrapper_function


# Decorator for checking if game not exists
def _game_not_exists(original_function):
    def wrapper_function(*args, **kwargs):
        if(game._game_thread is not None):
            if(game._game_thread.is_alive()):
                raise _PGCException('Game is running. Set it before you start the game.')
        else:
            return original_function(*args, **kwargs)
    return wrapper_function


# ########################################### GLOBAL PROPERTIES  #######################################################
class _GameProperties():
    def __init__(self):
        self._FPS = 60                      # Game FPS value
        self.start_map = 'Map0'             # Starting map name
        self._game_thread = None             # Thread that is running the game

        import gamecontrollermt.mainGame as _mainGame
        self.game_object = _mainGame.PyManMain(self._FPS, 70, 70)  # Game object

    @property
    def fps(self):
        return self._FPS

    @fps.setter
    def fps(self, value):
        self._FPS = value
        self.game_object.fps = value

    @property
    @_game_not_exists
    def w_offset(self):
        return self.game_object.w_offset

    @w_offset.setter
    @_game_not_exists
    def w_offset(self, value):
        self.game_object.w_offset = value

    @property
    @_game_not_exists
    def h_offset(self):
        return self.game_object.h_offset

    @h_offset.setter
    @_game_not_exists
    def h_offset(self, value):
        self.game_object.h_offset = value

    # Get, Add, Remove functions to/from before_start
    def get_before_start_func(self):
        return self.game_object.before_start

    def add_before_start_func(self, value):
        self.game_object.before_start.append(value)

    def remove_before_start_func(self, value):
        self.game_object.before_start.remove(value)

    # Get, Add, Remove functions to/from first_game_loop
    def get_first_game_loop_func(self):
        return self.game_object.first_game_loop

    def add_first_game_loop_func(self, value):
        self.game_object.first_game_loop.append(value)

    def remove_first_game_loop_func(self, value):
        self.game_object.first_game_loop.remove(value)

    # Get, Add, Remove functions to/from last_game_loop
    def get_last_game_loop_func(self):
        return self.game_object.last_game_loop

    def add_last_game_loop_func(self, value):
        self.game_object.last_game_loop.append(value)

    def remove_last_game_loop_func(self, value):
        self.game_object.last_game_loop.remove(value)

    # Get, Add, Remove functions to/from on_exit
    def get_on_exit_func(self):
        return self.game_object.on_exit

    def add_on_exit_func(self, value):
        self.game_object.on_exit.append(value)

    def remove_on_exit_func(self, value):
        self.game_object.on_exit.remove(value)

# ######### Object containing global properties
game = _GameProperties()


# ######### Colors definition
class _Color():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
colors = _Color()


# ##############################################  START GAME FUNCTION  #################################################
def start_game():
    import threading
    global game

    print('Starting map named ' + game.start_map + '.')

    if(game._game_thread is not None):
        if(not game._game_thread.is_alive()):
            game = _GameProperties()
        else:
            exit_game()
            _time.sleep(0.5)
            game = _GameProperties()

    game.game_object._createWorld(game.start_map)

    game._game_thread = threading.Thread(target=game.game_object._mainLoop, args=(), daemon=True)
    game._game_thread.start()


# ##############################################  GAME GETTER FUNCTIONS  ###############################################
# Exit running game
@_game_exists
def exit_game():
    global game
    game.game_object.gameExit = True
    game.game_object = None


# Start new game with a different map
@_game_exists
def change_map(name):
    global  game
    exit_game()
    _time.sleep(0.5)
    game = _GameProperties()
    game.start_map = name
    start_game()


# Returns array with all sprites created in game
@_game_exists
def get_all_ingame_objects():
    global game
    ret = []
    for group in game.game_object.worldList:
        for instance in group:
            ret.append(instance)
    return ret


# Returns array of all items created in game
@_game_exists
def get_items():
    global game
    ret = []
    for instance in game.game_object.itemList:
        ret.append(instance)
    return ret


# Returns array of all players created in game
@_game_exists
def get_player():
    global game
    ret = []
    for instance in game.game_object.playerList:
        ret.append(instance)
    return ret


# Returns array of all user objects created in game
@_game_exists
def get_custom_objects():
    global game
    ret = []
    for instance in game.game_object.userInstance:
        ret.append(instance)
    return ret

# Returns array of all actors except ripley created in game
@_game_exists
def get_actors():
    global game
    ret = []
    for instance in game.game_object.actorList:
        ret.append(instance)
    return ret


# Returns array of all walls created in game
@_game_exists
def get_walls():
    global game
    ret = []
    for instance in game.game_object.walls:
        ret.append(instance)
    return ret


# ##############################################  PGC GAME CLASSES  ####################################################
# Class represent item game objects
class Item(object):
    __metaclass__ = _abc.ABCMeta


# Class represent alien game objects
class Enemy(object):
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

    def setFont(self, font, size):
        self.font = pygame.font.SysFont(font, size)


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

        self.anim_speed = 3
        self.play_frame = round(game.fps / (frames * self.anim_speed))
        self.anim_frames = frames - 1
        self.current_frame = 1
        self.current_anim_frame = 0
        self.plus = True

    def setPingPong(self, value):
        self.pingpong = value

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


# ########################################### OVERWATCH FUNCTIONS ######################################################
def stop_overwatch():
    global _filewatch
    _filewatch.observer.stop()


def add_file_to_overwatch(file_name):
    global _filewatch
    _filewatch.add_file(file_name)


def remove_file_from_overwatch(file_name):
    global _filewatch
    _filewatch.remove_file(file_name)


def get_overwatch_files():
    global _filewatch
    return _filewatch.get_files()


# ########################################### OVERWATCH PRIVATE F ######################################################
class _MyHandler(_FileSystemEventHandler):
    def __init__(self):
        self._watchfiles = []
        self.observer = None

    def on_modified(self, event):
        for file in self._watchfiles:
            if(event.src_path.endswith(file)):
                try:
                    _reload(_sys.modules.get(file[:-3]))
                except Exception as exc:
                    print(exc)

    def add_file(self, file_name):
        self._watchfiles.append(file_name)

    def get_files(self):
        return self._watchfiles

    def remove_file(self, file):
        if(file in self._watchfiles):
            self._watchfiles.remove(file)

    def overwatch(self):
        path = _sys.argv[1] if len(_sys.argv) > 1 else '.'
        event_handler = self
        self.observer = _Observer()
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()


# ############################################# ON IMPORT EXECUTE ######################################################
# print('Thanks for using pgc interactive library.\nFor starting a game please use command start_game(\'Level name\').')
_filewatch = _MyHandler()
_filewatch.overwatch()


# ############################################## AT IPYTHON EXIT #######################################################
def _exit_function():
    if (game._game_thread is not None):
        if(game._game_thread.is_alive()):
            exit_game()
    stop_overwatch()

_atexit.register(_exit_function)
