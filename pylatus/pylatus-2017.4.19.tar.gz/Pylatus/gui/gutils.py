#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from PyQt5 import QtCore, QtWidgets


class GUtils:
    config = None

    @staticmethod
    def askPass(parent):
        if not GUtils.config:
            return False

        pas, ok = QtWidgets.QInputDialog.getText(parent, 'Password required',
                                                 'This operation requires a special permission:',
                                                 QtWidgets.QLineEdit.Password)
        pashash = hashlib.sha1(pas.encode('utf8', errors='ignore')).hexdigest()
        return GUtils.config.rootHash == pashash if ok else False

    @staticmethod
    def setConfig(config):
        GUtils.config = config

    @staticmethod
    def delay(msec):
        dieTime = QtCore.QTime.currentTime().addMSecs(msec)
        while QtCore.QTime.currentTime() < dieTime:
            QtCore.QCoreApplication.processEvents()


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __hash__(self):
        return id(self)
