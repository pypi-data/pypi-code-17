#!/usr/bin/python
# -*- coding: utf-8 -*-

import builtins
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from .. import scripo
from .auxscript import QPyCompletionTextEdit, QPyHighlighter
from .ui.ui_wscripted import Ui_WScriptEd


class WScriptEd(QtWidgets.QDialog, Ui_WScriptEd):
    sigClosed = QtCore.pyqtSignal()
    sigScript = QtCore.pyqtSignal(str)
    specialWords = ([
        'filename', 'folder', 'kappa', 'phi', 'omega', 'pldistf', 'pldistd', 'plvert', 'plrot', 'nframes', 'nperiods',
        'exposure', 'dOmega', 'setp', 'mout', 'rng', 'pid',
    ] + scripo.musst.specialWords +
        scripo.cryostream.specialWords +
        scripo.blower.specialWords +
        scripo.diffractometer.specialWords +
        scripo.motor.specialWords +
        scripo.lakeshore.specialWords
    )

    def __init__(self, parent, settings, userEnv):
        super().__init__(parent=parent)
        self.settings = settings
        self.motors = []
        self.setupUi(self)
        self.loadSettings()
        self.setEnv(userEnv)

    def setEnv(self, userEnv):
        keywords = list(userEnv.keys()) + self.specialWords
        self.scriptTextEdit = QPyCompletionTextEdit()
        self.scriptTextEdit.setCompleter(keywords + dir(builtins))
        font = QtGui.QFont()
        font.setFamily('Monospace')
        font.setPointSize(12)
        self.scriptTextEdit.setFont(font)
        self.scriptTextEdit.setObjectName('scriptTextEdit')
        self.verticalLayout.insertWidget(0, self.scriptTextEdit)
        self.highlighter = QPyHighlighter(sorted(keywords), self.scriptTextEdit)
        self.qMsgError = partial(QtWidgets.QMessageBox.critical, self, 'Script Error')

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()

    def saveSettings(self):
        s = self.settings
        s.setValue('WScriptEd/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WScriptEd/Geometry', QtCore.QByteArray()))

    @QtCore.pyqtSlot()
    def on_toSeqButton_clicked(self):
        self.sigScript.emit(self.scriptTextEdit.toPlainText())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
