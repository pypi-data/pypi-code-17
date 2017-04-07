#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.ui_wlogging import Ui_WLogging


class WLogging(QtWidgets.QDialog, Ui_WLogging):
    sigClosed = QtCore.pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.setupUi(self)
        self.loadSettings()
        self.out = None

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()
        super().closeEvent(event)

    def saveSettings(self):
        s = self.settings
        s.setValue('WLogging/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WLogging/Geometry', QtCore.QByteArray()))

    def postLogMessage(self, name, level, msg):
        self.loggingTextEdit.moveCursor(QtGui.QTextCursor.End)
        message = '{:%Y-%m-%d %H:%M:%S.%f} {}: {}: {}\n'.format(datetime.now(), level, name, msg)
        self.loggingTextEdit.insertPlainText(message)
        if self.out:
            self.out.write(message)
            self.out.flush()

    def setConfig(self, config):
        self.config = config
        self.setOut()

    def setOut(self):
        self.out = open(self.config.logFile, 'a+')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
