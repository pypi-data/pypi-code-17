# mad/__init__.py
#
#

""" bot classes. """

from .engine import Engine
from .error import ENOTIMPLEMENTED
from .utils import sname

class Bot(Engine):

    """
        main bot class.

        >>> from botlib.bot import Bot
        >>> bot = Bot()
        >>> bot.connect()

    """

    cc = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = str(type(self))
        self.channels = []
        self.cfg.fromdisk(self.type)

    def announce(self, txt):
        """ print text on joined channels. """
        if self.cfg.silent:
            return
        if not self.channels:
            self.raw(txt)
        for channel in self.channels:
            self.say(channel, txt)

    def connect(self, *args, **kwargs):
        """ connect to server. """
        self._connected.ready()

    def dispatch(self, event):
        self._counter.events += 1
        event.handle()

    def event(self, *args, **kwargs):
        """ virtual method returning a event from the bot. """
        raise ENOTIMPLEMENTED

    def exit(self):
        self.put(None)

    def id(self, *args, **kwargs):
        return sname(self).lower() + "." + (self.cfg.server or "localhost")

    def join(self, channel):
        """ join a channel. """
        pass

    def joinall(self):
        """ join all channels. """
        for channel in self.channels:
            self.join(channel)

    def raw(self, txt):
        """ send txt to server. """
        self._counter.raw += 1

    def prompt(self, colors=False):
        """ echo prompt to sys.stdout. """
        pass

    def say(self, channel, txt):
        """ say something on a channel. """
        self.raw(str(txt).strip())

    def start(self, *args, **kwargs):
        from .space import fleet
        super().start(*args, **kwargs)
        fleet.add(self)
