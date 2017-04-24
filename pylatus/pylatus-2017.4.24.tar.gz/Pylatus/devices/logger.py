#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial
from datetime import datetime
from PyQt5 import QtCore
from ..controller.config import Config


class _Logger(QtCore.QObject):
    sigPostLogMessage = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.out = None
        self.outName = ''
        self.sigPostLogMessage.connect(self._writeFile)

    def setConfig(self):
        if Config.LogFile and Config.LogFile != self.outName:
            try:
                self.out = open(Config.LogFile, 'a+')
                self.outName = Config.LogFile
                return
            except OSError:
                pass
        self.out = None
        self.outName = ''

    def log(self, name, level, msg):
        message = f'{datetime.now():%Y-%m-%d %H:%M:%S.%f} {level}: {name}: {msg}\n'
        self.sigPostLogMessage.emit(message)

    def error(self, name, msg):
        self.log('ERROR', name, msg)

    def info(self, name, msg):
        self.log('INFO', name, msg)

    def warning(self, name, msg):
        self.log('WARNING', name, msg)

    warn = warning

    def _writeFile(self, message):
        if self.out:
            self.out.write(message)
            self.out.flush()


class Logger:
    logger = _Logger()

    def __init__(self, name):
        self.log = partial(self.logger.log, name)
        self.info = partial(self.logger.info, name)
        self.error = partial(self.logger.error, name)
        self.warning = partial(self.logger.warning, name)
        self.warn = self.warning
