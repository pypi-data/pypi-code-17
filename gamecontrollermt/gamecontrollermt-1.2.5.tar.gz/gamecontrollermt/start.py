import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Define map defaults
DEFAULT_MAP = 'Map0.tmx'


class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self, fps=60, w_offset=100, h_offset=100):
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.w_offset = w_offset
        self.h_offset = h_offset
        self._width = 1
        self._height = 1

        """Set game related properties"""
        pygame.display.set_caption('Game Controller Master Thesis')
        self.fps = fps
        self.paused = False
        self.gameExit = False
        self.player = False

        """User functions to be executed"""
        self.before_start = []
        self.first_game_loop = []
        self.last_game_loop = []
        self.on_exit = []

        """Initialize game groups"""
        self.userInstance = pygame.sprite.Group()
        self.playerList = pygame.sprite.Group()
        self.itemList = pygame.sprite.Group()
        self.actorList = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        """Fill game groups"""
        self.worldList = []
        self.worldList.append(self.itemList)
        self.worldList.append(self.actorList)
        self.worldList.append(self.userInstance)
        self.worldList.append(self.playerList)
        self.worldList.append(self.walls)

        """Intialize properties"""
        self.screen = None
        self.background = None
        self.map = None
        self.map_img = None

    def _createWorld(self, map=None):
        from gamecontrollermt.mapLoader import TiledMap

        """Create and Fill the Screen"""
        self.screen = pygame.display.set_mode((self._width, self._height))

        """Setting Up Map"""
        if(map is None):
            self.map = TiledMap('data/Maps/' + DEFAULT_MAP, self, self._width, self._height)
        else:
            try:
                self.map = TiledMap('data/Maps/' + map + '.tmx', self, self._width, self._height)
            except Exception as ex:
                print(str(ex))
                self.map = TiledMap('data/Maps/' + DEFAULT_MAP, self, self._width, self._height)

        """Resize map accordingly to tiled map"""
        self.screen = pygame.display.set_mode((self.map.width + self.w_offset, self.map.height + self.h_offset))
        self._width = self.map.width + self.w_offset
        self._height = self.map.height + self.h_offset
        self.map.worldWidthZero = ((self._width) - self.map.width)/2
        self.map.worldHeightZero = ((self._height) - self.map.height)/2

        """Fill background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(BLACK)

        """Create and Spawn Map"""
        self.map_img = self.map._make_map()
        self.map._fill_map()

    def _mainLoop(self):
        for function in self.before_start:
            function()

        """This is the Main Loop of the Game"""
        clock = pygame.time.Clock()

        while not self.gameExit:
            for function in self.first_game_loop:
                function()

            """Pygame Events"""
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.gameExit = True

            if(self.paused):
                continue
            """Set game Frame rate"""
            clock.tick(self.fps)

            """Map blitting"""
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.map_img, (self.map.worldWidthZero, self.map.worldHeightZero))

            """Update Screen"""
            for group in self.worldList:
                group.update()
                group.draw(self.screen)

            pygame.display.flip()

            for function in self.last_game_loop:
                function()

        for function in self.on_exit:
            function()

        pygame.quit()

    def pause(self):
        self.paused = not self.paused

    def add_group(self, group):
        self.worldList.append(group)

    def add_actor_to_game(self, actor_name, x, y, width=0, height=0, object_properties=[]):
        self.map.add_actor_to_map(actor_name, x, y, width, height, object_properties)

    def add_to_group(self, actor, group):
        if (not (actor in group)):
            group.add(actor)

    def remove_from_group(self, actor, group):
        if(actor in group):
            group.remove(actor)

# if __name__ == "__main__":
#     MainWindow = PyManMain()
#     MainWindow._createWorld()
#     MainWindow._mainLoop()
