#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from .ui.ui_wabout import Ui_WAbout


class WAbout(QtWidgets.QDialog, Ui_WAbout):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()
