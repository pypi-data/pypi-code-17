import sys as _sys
import time as _time
import atexit as _atexit
from importlib import import_module as _imp
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
class _GameProperties(object):
    def __init__(self):
        self._FPS = 60                      # Game FPS value
        self.start_map = 'Map0'             # Starting map name
        self._game_thread = None            # Thread that is running the game

        from gamecontrollermt import start
        self.game_object = start.PyManMain(self._FPS, 70, 70)  # Game object

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
class _Color(object):
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
colors = _Color()


# #####################################################  GAME FUNCTION  ################################################
def start_game():
    import threading
    from gamecontrollermt import start
    global game

    print('Starting map named ' + game.start_map + '.')

    if(game._game_thread is not None):
        if(not game._game_thread.is_alive()):
            game.game_object = start.PyManMain(game._FPS, 70, 70)
        else:
            exit_game()
            _time.sleep(0.5)
            game.game_object = start.PyManMain(game._FPS, 70, 70)

    game.game_object._createWorld(game.start_map)

    game._game_thread = threading.Thread(target=game.game_object._mainLoop, args=(), daemon=True)
    game._game_thread.start()


# Exit running game
@_game_exists
def exit_game():
    global game
    game.game_object.gameExit = True
    game._game_thread.join()
    game.game_object = None


# Start new game with a different map
@_game_exists
def change_map(name):
    from gamecontrollermt import start
    global game
    exit_game()
    _time.sleep(0.5)
    game.game_object = start.PyManMain(game._FPS, 70, 70)
    game.start_map = name
    start_game()


# ##############################################  GAME GETTER FUNCTIONS  ###############################################
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
def get_iactors():
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


# ########################################### ADD TO WORLD FUNCTION ####################################################
def add_actors(name:str, x, y, props):
    global game
    game.game_object.add_actor_to_game(name, x, y, object_properties=props)


def add_actoro(actor:object, group):
    global game
    actor.world = game.game_object
    game.game_object.add_to_group(actor, group)

# ########################################### OVERWATCH FUNCTIONS ######################################################
_watchfiles = []


def start_overwatch():
    global _filewatch
    _filewatch = _MyHandler(_watchfiles)
    _filewatch.overwatch()


def stop_overwatch():
    global _filewatch
    _filewatch.observer.stop()
    print('[Overwatch]: Overwatch stopped.')


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
    def __init__(self, watchfiles):
        self._watchfiles = watchfiles
        self.observer = None

    def on_modified(self, event):
        for file in self._watchfiles:
            if(event.src_path.endswith(file)):
                rfile = _sys.modules.get(file[:-3])
                if(rfile is None):
                    _imp(file[:-3])
                    print('[Overwatch] ' + str(file) + ' imported.')
                else:
                    try:
                        _reload(rfile)
                        print('[Overwatch] ' + str(rfile) + ' reloaded.')
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
        self.observer.schedule(event_handler, path, recursive=False)
        self.observer.start()

# ############################################# ON IMPORT EXECUTE ######################################################
print('Hello, Welcome to pgc interactive library.')
print('For starting a game please use command pgc.start_game().')
start_overwatch()
print('[Overwatch]: Overwatch started.')


# ############################################## AT IPYTHON EXIT #######################################################
def _exit_function():
    global _filewatch
    if (game._game_thread is not None):
        if(game._game_thread.is_alive()):
            exit_game()
    print('Thanks for using pgc interactive library.')
    if(_filewatch.observer.isAlive()):
        stop_overwatch()

_atexit.register(_exit_function)
