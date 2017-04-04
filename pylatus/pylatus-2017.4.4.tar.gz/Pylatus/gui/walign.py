#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .qmotordialog import QMotorDialog
from .ui.ui_walign import Ui_WBeamAlign


class WAlign(QMotorDialog, Ui_WBeamAlign):
    def __init__(self, parent, settings):
        super().__init__(parent, 'SpinBox')
        self.settings = settings
        self.setupUi(self)

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()

    def saveSettings(self):
        s = self.settings
        s.setValue('WAlign/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WAlign/Geometry', QtCore.QByteArray()))
