# clock.py
#
#

""" timer, repeater and other clock based classes. """

from .event import Event
from .object import Default, Config, Object
from .utils import name , get_day, get_hour, to_day, elapsed, now, to_time, day 

import threading
import logging
import time
import os

start = 0

class Timer(Object):

    """
        call a function as x seconds of sleep.

    """

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(**kwargs)
        self._state = Default(default="")
        self._counter = Default(default=0)
        self._time = Default(default=0)
        self._time.start = time.time()
        self._time.latest = time.time()
        self._state.status = "waiting"
        self._name = kwargs.get("name", name(func))
        self.sleep = sleep
        self.func = func
        self.args = args
        try:
            self._event = self.args[0]
            logging.warn(self._event)
            self._state.origin = self._event.origin
        except:
            self._event = Event()
        self.kwargs = kwargs

    def start(self):
        """ start the timer. """
        timer = threading.Timer(self.sleep, self.run)
        timer.setDaemon(True)
        timer.setName(self._name)
        timer.sleep = self.sleep
        timer._state = self._state
        timer._name = self._name
        timer._time = self._time
        timer._counter = self._counter
        self._counter.run += 1
        self._time.latest = time.time()
        timer.start()
        return timer

    def run(self, *args, **kwargs):
        """ run the registered function. """
        self._time.latest = time.time()
        self.func(*self.args, **self.kwargs)
 
    def exit(self):
        """ cancel the timer. """
        self._status = ""
        self.cancel()

class Repeater(Timer):

    """
        Repeat an funcion every x seconds. 

        >>> def func(event): event.reply("yo!")

        >>> from bot.clock import Repeater
        >>> from bot.time import now
        >>> repeater = Repeater(now(), func)
        >>> repeater.start()[B

    """
    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func, *args, **kwargs) 

    def run(self, *args, **kwargs):
        self._time.start = time.time()
        self._time.run += 1
        try:
            self.func(*self.args, **self.kwargs)
        except:
            logging.error(get_exception())
        self.start()

def init(event):
    from .space import cfg, db, kernel
    cfg = Config(default=0).load(os.path.join(cfg.workdir, "runtime", "timer"))
    cfg.template("timer")
    timers = []
    for e in db.sequence("timer", cfg.latest):
        if e.done: continue
        if "time" not in e: continue
        if time.time() < int(e.time):
            timer = Timer(int(e.time), e.direct, e.txt)
            t = kernel.launch(timer.start)
            timers.append(t)
        else:
            cfg.last = int(e.time)
            cfg.save()
            e.done = True
            e.sync()
    return timers

def timer(event):
    """ timer command to schedule a text to be printed on a given time. stopwatch to measure elapsed time. """
    if not event._parsed.rest:
        event.reply("timer <string with time>")
        return
    seconds = 0
    line = ""
    for word in event._parsed.args:
        if word.startswith("+"):
             try:
                 seconds = int(word[1:])
             except:
                 event.reply("%s is not an integer" % seconds)
                 return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event._parsed.rest)
        except ENODATE:
            try:
                target = to_day(day())
            except ENODATE:
                pass
        try:
            hour =  get_hour(event._parsed.rest)
            if hour:
                target += hour
        except ENODATE:
            pass
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    e = Event(event)
    e.services = "clock"
    e._prefix = "timer"
    e.txt = event._parsed.rest
    e.time = target
    e.done = False
    e.save()
    timer = Timer(target - time.time(), e.direct, e.txt)
    kernel.launch(timer.start)
    event.ok(time.ctime(target))

def begin(event):
    """ begin stopwatch. """
    global start
    try:
        start = to_time(now())
    except ENODATE:
        event.reply("can't detect date from %s" % event.txt)
        return
    event.reply("time is %s" % time.ctime(start))

def end(event):
    """ stop stopwatch. """
    diff = time.time() - start
    if diff:
        event.reply("time elapsed is %s" % elapsed(diff))
