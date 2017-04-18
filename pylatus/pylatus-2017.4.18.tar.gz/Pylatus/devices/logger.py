#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class Logger(QtCore.QObject):
    sigPostLogMessage = QtCore.pyqtSignal(str, str, str)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def log(self, msgType, msg):
        self.sigPostLogMessage.emit(self.name, msgType, msg)

    def error(self, msg):
        self.log('ERROR', msg)

    def info(self, msg):
        self.log('INFO', msg)

    def warning(self, msg):
        self.log('WARNING', msg)

    warn = warning
