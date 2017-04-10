import logging
import os
import time

_log = logging.getLogger('FileWatcher')
IS_FILE = 0
IS_LINK = 1
IS_MOUNT = 2
IS_DIR = 3

DELETED = 0
MODIFIED = 1
LAST_ACCESS = 2
SIZE = 3
META = 4
CHANGE_OBJTYPE = 5


class RemoveWatcher(Exception):
    pass


class FileWatcher:
    def __init__(self, sleep=1):
        self.sleep = sleep

        self.watch_list = []
        self.read = False

    def _default_handler(self, file):
        def check_type():
            if file.obj_type is not None:
                return ['File', 'Symlink', 'MountPoint', 'Dir'][file.obj_type]
            return 'Path'

        def check_mode():
            if DELETED in file.changes:
                return 'deleted'
            elif MODIFIED in file.changes:
                return 'modified'
            return '|'.join(map(str, file.changes))

        _log.warning(f"{check_type()} '{file.name}' was {check_mode()}")

    def get_by_filename(self, filename, insert=True):
        for file in self.watch_list:
            if file.name == filename:
                return file
        if insert:
            file = File(filename)
            self.watch_list.append(file)
            return file
        return None

    def watch(self, filename, handler=None):
        file = self.get_by_filename(filename)
        _log.debug(f"Watch '{file.name}'")
        file.subscribe(handler)
        file.subscribe(self._default_handler)

    def remove(self, target):
        if isinstance(target, File) and target in self.watch_list:
            self.watch_list.remove(target)
            _log.debug(f"Stop watching '{target.name}'")
            return True
        elif isinstance(target, str):
            file = self.get_by_filename(target, False)
            _log.debug(f"Stop watching '{file.name}'")
            if not file:
                return False
            self.remove(file)
            return True
        raise KeyError(target)

    def stop(self):
        self.read = False

    def serve(self):
        self.read = True

        _log.debug(f"FileWatcher was started")
        while self.read:
            for file in self.watch_list:
                try:
                    if file.check():
                        file.trigger()
                except RemoveWatcher:
                    self.remove(file)
                except SystemExit:
                    raise
                except:
                    _log.exception('Check error')
                    self.remove(file)
            self.do_sleep()
        _log.debug(f"FileWatcher was stopped")

    def do_sleep(self):
        time.sleep(self.sleep)


class File:
    def __init__(self, name):
        self.ready = False
        self.name = os.path.abspath(name)
        if not os.path.exists(self.name):
            raise OSError('File or directory "' + self.name + '" is not found!')

        self.meta = None
        self.last_change = None
        self.last_access = None
        self.size = 0
        self.obj_type = None
        self.exist = True

        self._file = None

        self.handlers = []
        self.changes = set()

        self._check(True)

        self.changes.clear()
        self.ready = True

    def subscribe(self, handler):
        if callable(handler) and handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler):
        self.handlers.remove(handler)

    def trigger(self):
        for handler in self.handlers:
            try:
                handler(self)
            except:
                self.unsubscribe(handler)
                raise
        self.changes.clear()

    def check(self, full=False):
        if not self.ready:
            return False
        ch = self._check(full)
        if ch and not full:
            self.check(True)
        return ch

    def _check(self, full=False):
        ch_exist = self._check_exist()
        if self.exist:
            self._check_modified()
            if full or ch_exist:
                self._check_access()
                self._check_meta()
                self._check_objtype()
                self._check_size()
        if ch_exist and not self.exist:
            self.last_change = None
            self.last_access = None
            self.meta = None
            self.obj_type = None
            self.size = 0
            self.changes.add(MODIFIED)
            self.changes.add(LAST_ACCESS)
            self.changes.add(META)
            self.changes.add(CHANGE_OBJTYPE)
            self.changes.add(SIZE)

        if self.changes:
            return True
        return False

    def _check_exist(self):
        exist = os.path.exists(self.name)
        if exist != self.exist:
            self.exist = exist
            self.changes.add(DELETED)
            return True
        return False

    def _check_objtype(self):
        if os.path.isfile(self.name):
            obj_type = IS_FILE
        elif os.path.islink(self.name):
            obj_type = IS_LINK
        elif os.path.ismount(self.name):
            obj_type = IS_MOUNT
        else:
            obj_type = IS_DIR

        if obj_type != self.obj_type:
            self.obj_type = obj_type
            self.changes.add(CHANGE_OBJTYPE)
            return True
        return False

    def _check_size(self):
        size = os.path.getsize(self.name)
        if size != self.size:
            self.size = size
            self.changes.add(SIZE)
            return True
        return False

    def _check_meta(self):
        meta = os.path.getctime(self.name)
        if meta != self.meta:
            self.meta = meta
            self.changes.add(META)
            return True
        return False

    def _check_modified(self):
        changed = os.path.getmtime(self.name)
        if changed != self.last_change:
            self.last_change = changed
            self.changes.add(MODIFIED)
            return True
        return False

    def _check_access(self):
        access = os.path.getatime(self.name)
        if access != self.last_access:
            self.last_access = access
            self.changes.add(LAST_ACCESS)
            return True
        return False

    def __str__(self):
        if self.obj_type is not None:
            obj_type = ['File', 'Symlink', 'MountPoint', 'Dir'][self.obj_type]
        else:
            obj_type = 'Path'
        return f"<{obj_type} '{self.name}' {self.size} bytes {self.last_change}>"
