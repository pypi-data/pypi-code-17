#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
import aspic


class Monitor(QtCore.QObject):
    sigMonitorConnected = QtCore.pyqtSignal(str)
    sigMonitorValue = QtCore.pyqtSignal(int)
    sigMonitorError = QtCore.pyqtSignal(str)
    secName = 'sec'

    def __init__(self):
        super().__init__()
        self.config = None
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

    def setConfig(self, config):
        self.config = config
        if self.oldConnection and self.oldConnection != self.config.monitorSpec:
            self.connectToSpec()

    def connectToSpec(self):
        if not self.config:
            return
        self.oldConnection = self.config.monitorSpec
        host, spec, counter = self.config.monitorSpec.split(':')
        self.sec = aspic.Qounter((host, spec), self.secName)
        self.mon = aspic.Qounter((host, spec), counter)
        self.sec.sigValueChanged.connect(self.monChanged)
        self.mon.sigValueChanged.connect(self.monChanged)
        self.mon.sigConnected.connect(self.sigMonitorConnected.emit)
        self.mon.sigError.connect(self.sigMonitorError.emit)

    def monChanged(self, name, counts):
        if self.running:
            if name == self.secName and counts >= self.countTime:
                self.ready = True
            elif name == self.mon.name() and self.ready:
                self.ready = False
                self.sigMonitorValue.emit(int(counts))
                self.count()

    def count(self):
        if self.running and self.sec.isConnected() and self.mon.isConnected():
            self.mon.count(self.countTime)
