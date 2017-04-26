# botlib/watcher.py
#
#

""" watch files. """

from .clock import Repeater
from .object import Object
from .engine import Engine
from .space import cfg, db, launcher, partyline, runtime

import select
import time
import os

def out(txt):
    for orig, sockets in partyline.items():
        for sock in sockets:
            sock.write(txt)
            sock.flush()

class Watcher(Object):

    def start(self):
        fd = []
        for fn in self.watchlist():
            f = open(fn)
            fd.append(f.fileno())
            if cfg.verbose:
                print("# watcher on %s" % fn)
            launcher.launch(self.listen, fn)
            
    def listen(self, fn):
        f = open(fn)
        p = 0
        while True:
            f.seek(p)
            latest_data = f.readline()
            p = f.tell()
            if latest_data:
                out(latest_data)
            time.sleep(1.0)
                            
    def watchlist(self):
        for obj in db.find("watch"):
            yield obj.watch

def init(event):
    watcher = Watcher()
    return launcher.launch(watcher.start)
