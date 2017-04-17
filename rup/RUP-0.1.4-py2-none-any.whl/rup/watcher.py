import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from util import determine_run_number, is_data, is_rup, is_run_log, is_log
import logging
import threading


class WatchedFile:

    def __init__(self, path, n):
        self.path = path
        self.n = n
        self.mod_time = None
        self.print_time = -1
        self.reset_mod_time()
        self.is_data = is_data(path)
        self.is_rup = not self.is_data

    def reset_mod_time(self):
        self.mod_time = time.time()

    def reset_print_time(self):
        self.print_time = time.time()


class Watcher:

    def __init__(self, directory, timeout):
        self.observer = Observer()
        self.directory = directory
        self.event_handler = None
        self.timeout = timeout
        self._observers = []
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.info("Watching {} with timeout {}".format(self.directory, self.timeout))

    def run(self):
        self.event_handler = WatcherEventHandler()
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()

        t = threading.Thread(target=self.__watch)
        t.daemon = True
        t.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def add_observer(self, obs):
        self._observers.append(obs)

    def __watch(self):
        handler = self.event_handler

        trash = []

        while True:
            try:
                for key, f in handler.watching.iteritems():
                    diff = int(time.time() - f.mod_time)
                    self.logging.info("{} is {} seconds old".format(f.path, diff))
                    if diff > self.timeout:
                        trash.append(key)
                        self.logging.info("{} is {} seconds old. Retiring.".format(f.path, diff))
                        self.notify_observes(f)

                for key in trash:
                    handler.watching.pop(key)

                trash = []

                time.sleep(5)
            except Exception as e:
                self.logging.error(e.message)

    def notify_observes(self, f):
        for obs in self._observers:
            try:
                obs(f)
            except Exception as e:
                self.logging.error("Notifying observer failed:")
                self.logging.error(e)


class WatcherEventHandler(FileSystemEventHandler):

    def __init__(self):
        self.watching = {}
        self.logging = logging.getLogger(self.__class__.__name__)

    def on_any_event(self, event):
        event_type = event.event_type
        if event.is_directory or event_type == 'deleted':
            return None

        if event_type == 'moved':
            path = event.dest_path
        else:
            path = event.src_path

        if is_data(path) or is_rup(path) or is_log(path):
            n = determine_run_number(path)
        elif is_run_log(path):
            n = -1
        else:
            self.logging.info("{} is not recognized".format(path))
            return

        run = self.watching.get(path, WatchedFile(path, n))
        if time.time() - run.print_time > 1 or event_type == "created":
            self.logging.info("{} {}".format(path, event_type))
            run.reset_print_time()

        run.reset_mod_time()
        self.watching[path] = run

