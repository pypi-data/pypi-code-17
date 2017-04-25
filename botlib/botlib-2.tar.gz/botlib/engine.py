# mad/engine.py
#
#

""" 
    a engine is select.epoll event loop, easily interrup_table
    esp. versus a blocking event loop.

"""

from .error import EDISCONNECT, ERESUME
from .launcher import Launcher
from .handler import Handler
from .object import Object

import logging
import select
import time

class Engine(Handler, Launcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._poll = select.epoll()
        self._resume = Object()
        self._state.status = "running"
        self._time.start = time.time()
        self._connected.clear()

    def dispatch(self, event):
        event.handle()

    def select(self):
        while self._state.status:
            for event in self.events():
                if not event:
                    break
                self.dispatch(event)
                self._time.latest = time.time()

    def events(self):
        res = self._poll.poll()
        try:
            yield self.event()
        except (ConnectionResetError,
                BrokenPipeError,
                EDISCONNECT) as ex:
                    self.connect()

    def register_fd(self, f):
        try:
            fd = f.fileno()
        except:
            fd = f
        if not fd:
            return fd
        logging.warn("# engine on %s" % str(fd))
        self._poll.register(fd, select.EPOLLET)
        self._resume.fd = fd
        return fd

    def resume(self):
        if not self._resume.fd:
            raise bot.error.ERESUME
        logging.info("# resume on %s" % self._resume.fd)
        self._poll = select.epoll.fromfd(self._resume.fd)

    def start(self, *args, **kwargs):
        self.launch(self.select)
        super().start(*args, **kwargs)

    def stop(self):
        self._status = ""
        self._poll.close()
        super().stop()
