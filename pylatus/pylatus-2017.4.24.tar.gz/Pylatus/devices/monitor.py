#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
import aspic
from ..controller.config import Config


class Monitor(QtCore.QObject):
    sigConnected = QtCore.pyqtSignal(str)
    sigValue = QtCore.pyqtSignal(int)
    sigError = QtCore.pyqtSignal(str)
    secName = 'sec'

    def __init__(self):
        super().__init__()
        self.ready = False
        self.countTime = 0
        self.running = False
        self.oldConnection = ''

    def run(self, countTime):
        self.countTime = countTime
        self.running = True
        self.count()

    def abort(self):
        self.running = False

    def setConfig(self):
        if self.oldConnection and self.oldConnection != Config.MonitorSpec:
            self.connectToSpec()

    def connectToSpec(self):
        if Config.MonitorSpec:
            self.oldConnection = Config.MonitorSpec
            host, spec, counter = Config.MonitorSpec.split(':')
            self.sec = aspic.Qounter((host, spec), self.secName)
            self.mon = aspic.Qounter((host, spec), counter)
            self.sec.sigValueChanged.connect(self.monChanged)
            self.mon.sigValueChanged.connect(self.monChanged)
            self.mon.sigConnected.connect(self.sigConnected.emit)
            self.mon.sigError.connect(self.sigError.emit)

    def monChanged(self, name, counts):
        if self.running:
            if name == self.secName and counts >= self.countTime:
                self.ready = True
            elif name == self.mon.name() and self.ready:
                self.ready = False
                self.sigValue.emit(int(counts))
                self.count()

    def count(self):
        if self.running and self.sec.isConnected() and self.mon.isConnected():
            self.mon.count(self.countTime)
