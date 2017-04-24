#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.ui_wlogging import Ui_WLogging
from ..controller.config import Config


class WLogging(QtWidgets.QDialog, Ui_WLogging):
    sigClosed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.loadSettings()

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()
        super().closeEvent(event)

    def saveSettings(self):
        s = Config.Settings
        s.setValue('WLogging/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = Config.Settings
        self.restoreGeometry(s.value('WLogging/Geometry', Config.QBA))

    def postLogMessage(self, message):
        self.loggingTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.loggingTextEdit.insertPlainText(message)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
