#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from ..controller.config import Config
from .ui.ui_options import Ui_Ui_Settings


class WOptions(QtWidgets.QDialog, Ui_Ui_Settings):
    sigConfig = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setUI()

    def setUI(self):
        self.setupUi(self)
        self.editReadout1.setValidator(QtGui.QDoubleValidator())
        self.editReadout2.setValidator(QtGui.QDoubleValidator())
        self.editSeparator.setValidator(QtGui.QIntValidator())
        self.editNoBeamCounts.setValidator(QtGui.QIntValidator())
        self.editMusstTimeout1.setValidator(QtGui.QDoubleValidator())
        self.editMusstTimeout2.setValidator(QtGui.QDoubleValidator())
        self.editNumberOfFilters.setValidator(QtGui.QIntValidator())
        self.editBeamstopOn.setValidator(QtGui.QDoubleValidator())
        self.editBeamstopOff.setValidator(QtGui.QDoubleValidator())
        self.editScanTime.setValidator(QtGui.QDoubleValidator())
        self.editScanRange.setValidator(QtGui.QDoubleValidator())
        self.editScanStep.setValidator(QtGui.QDoubleValidator())
        self.editScanFilter.setValidator(QtGui.QIntValidator())
        self.editCommTimeout.setValidator(QtGui.QIntValidator())

    def loadSettings(self):
        s = Config.Settings
        self.restoreGeometry(s.value('WOptions/Geometry', Config.QBA))
        for name in self.__dict__:
            widget = self.__dict__[name]
            if isinstance(widget, QtWidgets.QLineEdit):
                name = name[4:]
                value = s.value(f'WOptions/{name}', getattr(Config, name))
                widget.setText(value)
                setattr(Config, name, value)
        self.saveSettings()

    def saveSettings(self):
        s = Config.Settings
        s.setValue('WOptions/Geometry', self.saveGeometry())
        for name in self.__dict__:
            widget = self.__dict__[name]
            if isinstance(widget, QtWidgets.QLineEdit):
                value = widget.text()
                name = name[4:]
                s.setValue(f'WOptions/{name}', value)
                setattr(Config, name, value)
        self.sigConfig.emit()

    @QtCore.pyqtSlot()
    def on_applyButton_clicked(self):
        self.saveSettings()
        self.close()

    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()

    def showEvent(self, event):
        self.loadSettings()
        super().showEvent(event)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.hide()
        self.saveSettings()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
