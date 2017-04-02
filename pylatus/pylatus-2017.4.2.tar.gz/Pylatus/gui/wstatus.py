#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .qmotordialog import QMotorDialog
from .ui.ui_wstatus import Ui_WStatus


class WStatus(QMotorDialog, Ui_WStatus):
    sigOpenShutter = QtCore.pyqtSignal()
    sigCloseShutter = QtCore.pyqtSignal()

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
        s.setValue('WStatus/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WStatus/Geometry', QtCore.QByteArray()))

    @QtCore.pyqtSlot()
    def on_shutterButton_clicked(self):
        if self.shutterButton.text() == 'Open shutter':
            self.openShutterSignal.emit()
            self.shutterButton.setText('Close shutter')
        else:
            self.closeShutterSignal.emit()
            self.shutterButton.setText('Open shutter')
