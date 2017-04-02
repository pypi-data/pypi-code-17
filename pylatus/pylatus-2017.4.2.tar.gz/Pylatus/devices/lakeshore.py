#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtNetwork


class Lakeshore(QtCore.QObject):
    heaterRange = 'Off', 'Low', 'Medium', 'High'
    sigStatus = QtCore.pyqtSignal(float, float)
    sigError = QtCore.pyqtSignal(str)
    sigParams = QtCore.pyqtSignal(float, float, float, float, int, float)
    STARTING_PARAMS = 1
    ENDING_PARAMS = 2
    STARTING_TEMP = 3
    ENDING_TEMP = 4

    def __init__(self):
        super().__init__()
        self.auxTimer = QtCore.QTimer(self)
        # noinspection PyUnresolvedReferences
        self.auxTimer.timeout.connect(self._send)
        self.lakeTimer = QtCore.QTimer(self)
        self.lakeTimer.setInterval(1000)
        self.auxTimer.setInterval(100)
        # noinspection PyUnresolvedReferences
        self.lakeTimer.timeout.connect(self.poll)
        self.temp = self.heater = 0
        self.p = self.i = self.d = 0
        self.mout = self.setp = self.range = 0

    # noinspection PyUnresolvedReferences
    def start(self, output, sensor, host, port=7777):
        self.callback = None
        self.queue = []
        self.output = output
        self.sensor = sensor
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.setProxy(QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.NoProxy))
        self.socket.connected.connect(self.sendFirstRequest)
        self.socket.readyRead.connect(self.readResponse)
        self.socket.disconnected.connect(self.stop)
        self.socket.error.connect(self.serverHasError)
        self.socket.connectToHost(host, port)

    def sendFirstRequest(self):
        self.lakeTimer.start()
        self.auxTimer.start()
        self.updateParameters()
        self.getHeater()
        self.getTemp()

    def readResponse(self):
        response = bytes(self.socket.readAll()).decode(errors='ignore')
        if self.callback is not None:
            self.callback(response)
            self.callback = None

    def serverHasError(self):
        msg = self.socket.errorString()
        self.sigError.emit(f'Cannot connect to Lakeshore:\n{msg}')
        self.stop()

    def stop(self):
        if self.lakeTimer.isActive():
            self.lakeTimer.stop()
            self.auxTimer.stop()
            self.socket.close()

    def send(self, cmd, callback=None):
        self.queue.append((cmd, callback))

    def _send(self):
        if not self.queue or self.callback is not None:
            return
        cmd, self.callback = self.queue.pop(0)
        if cmd == self.STARTING_PARAMS:
            pass
        elif cmd == self.ENDING_PARAMS:
            self.sigParams.emit(self.p, self.i, self.d, self.mout, self.range, self.setp)
        elif cmd == self.STARTING_TEMP:
            pass
        elif cmd == self.ENDING_TEMP:
            self.sigStatus.emit(self.temp, self.heater)
        else:
            self.socket.write(f'{cmd}\r\n'.encode())

    def poll(self):
        self.send(self.STARTING_TEMP)
        self.getTemp()
        self.getHeater()
        self.send(self.ENDING_TEMP)

    def getRange(self):
        self.send(f'RANGE? {self.output}', lambda v: setattr(self, 'range', float(v)))

    def setRange(self, value):
        self.send(f'RANGE {self.output},{value:.2f}')

    def getTemp(self):
        self.send(f'KRDG? {self.sensor}', lambda v: setattr(self, 'temp', float(v)))

    def getHeater(self):
        self.send(f'HTR? {self.output}', lambda v: setattr(self, 'heater', float(v)))

    def getMout(self):
        self.send(f'MOUT? {self.output}', lambda v: setattr(self, 'mout', float(v)))

    def setMout(self, value):
        self.send(f'MOUT {self.output},{value:.2f}')

    def getPID(self):
        def callback(response):
            self.p, self.i, self.d = [float(v) for v in response.split(',')]
        self.send(f'PID? {self.output}', callback)

    def setPID(self, p, i, d):
        self.send(f'PID {self.output},{p:f},{i:f},{d:f}')

    def getSetP(self):
        self.send(f'SETP? {self.output}', lambda v: setattr(self, 'setp', float(v)))

    def setSetp(self, value):
        self.send(f'SETP {self.output},{value:.1f}')

    def updateParameters(self):
        self.send(self.STARTING_PARAMS)
        self.getPID()
        self.getMout()
        self.getRange()
        self.getSetP()
        self.send(self.ENDING_PARAMS)

    def setParams(self, p, i, d, mout, rang, setp):
        self.setPID(p, i, d)
        self.setMout(mout)
        self.setRange(rang)
        self.setSetp(setp)

    def setSensor(self, sensor):
        self.sensor = sensor

    def setOutput(self, output):
        self.output = output
