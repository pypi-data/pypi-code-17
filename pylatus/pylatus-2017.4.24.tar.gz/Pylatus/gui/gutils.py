#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import hashlib
from PyQt5 import QtCore, QtWidgets
from ..controller.config import Config


class GUtils:
    @staticmethod
    def askPass(parent):
        pas, ok = QtWidgets.QInputDialog.getText(parent, 'Password required',
                                                 'This operation requires a special permission:',
                                                 QtWidgets.QLineEdit.Password)
        pashash = hashlib.sha1(pas.encode('utf8', errors='ignore')).hexdigest()
        return Config.RootHash == pashash if ok else False

    @staticmethod
    def delay(msec):
        dieTime = QtCore.QTime.currentTime().addMSecs(msec)
        while QtCore.QTime.currentTime() < dieTime:
            QtCore.QCoreApplication.processEvents()


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__uuid = uuid.uuid4()

    def __hash__(self):
        return hash(self.__uuid)
