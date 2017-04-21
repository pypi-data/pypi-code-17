# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.FixedRateTimer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Fixed rate timer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
from threading import Thread, Event, Lock

from .INotifiable import INotifiable
from .IClosable import IClosable

class Timer(Thread):

    def __init__(self, interval, callback):
        Thread.__init__(self)
        self._interval = interval
        self._callback = callback
        self._event = Event()

    def run(self):
        while not self._event.is_set():
            self._callback()
            time.sleep(self._interval)

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self._event.set()
            # block calling thread until thread really has terminated
            self.join()

class FixedRateTimer(object, IClosable):
    task = None
    delay = None
    interval = None
    started = False
    
    _timer = None
    _lock = None

    def __init__(self, task = None, interval = None, delay = None):
        self._lock = Lock()
        self.task = task
        self.delay = delay
        self.interval = interval
        self.started = False

    def start(self):
        self._lock.acquire()
        try:
            # Stop previously set timer
            if self._timer != None:
                self._timer.stop()
                self._timer = None

            # Set a new timer
            self._timer = Timer(self.delay / 1000, self._timer_callback)
            self._timer.start()
            
            # Set started flag
            self.started = True
        finally:
            self._lock.release()


    def _timer_callback(self):
        try:
            self.task.notify("pip-commons-timer")
        except:
            # Ignore or better log
            pass

    def stop(self):
        self._lock.acquire()
        try:
            # Stop the timer
            if self._timer != None:
                self._timer.stop()
                self._timer = None
            
            # Unset started flag
            self.started = False
        finally:
            self._lock.release()

    def close(self, correlation_id):
        self.stop()

