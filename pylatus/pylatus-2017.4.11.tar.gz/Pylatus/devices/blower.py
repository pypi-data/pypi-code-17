#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
import aspic


class Blower(QtCore.QObject):
    sigTemperature = QtCore.pyqtSignal(float)
    sigError = QtCore.pyqtSignal(str)
    sigConnected = QtCore.pyqtSignal()
    secCounterValue = 0.001

    def __init__(self):
        super().__init__()
        self.temp = 0
        self.target = 0
        self.ramp = 0
        self.running = False
        self.ready = False
        self.timer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.runCounter)

    def runCounter(self):
        self.ceuro.count(self.secCounterValue)

    def setConnected(self):
        if self.ceuro.isConnected() and self.meuro.isConnected():
            self.running = True
            self.timer.start(500)
            self.sigConnected.emit()

    def error(self, msg):
        self.stop()
        self.sigError.emit(msg)

    def checkCounterValue(self, name, value):
        if self.running and name == self.ceuro.name():
            self.temp = value
            self.sigTemperature.emit(value)

    def connectToSpec(self, host, session, motor, counter, rampcmd):
        self.rcmd = rampcmd
        self.ceuro = aspic.Qounter((host, session), counter)
        self.ceuro.sigError.connect(self.error)
        self.ceuro.sigConnected.connect(self.setConnected)
        self.ceuro.sigValueChanged.connect(self.checkCounterValue)
        self.rampCmd = aspic.Qommand(self.ceuro.connection())
        self.meuro = aspic.QMotor((host, session), motor)
        self.meuro.sigConnected.connect(self.setConnected)
        self.meuro.sigError.connect(self.error)

    def stop(self):
        self.running = False
        self.timer.stop()

    def setRamp(self, value):
        if self.running:
            self.rampCmd.run(self.rcmd.format(value))

    def run(self, target, ramp):
        if self.running:
            self.target = target
            self.ramp = ramp
            self.setRamp(ramp)
            self.meuro.move(target)

    def pause(self):
        self.run(self.temp, self.ramp)

    def resume(self):
        self.run(self.target, self.ramp)
