#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import uuid
import concurrent.futures
from PyQt5 import QtCore
import numpy as np
from scipy import optimize
from cryio import cbfimage


def gauss(x, xc, w, a):
    return a * np.exp(-(x - xc) ** 2 / (2 * w ** 2))


class ScanManager(QtCore.QObject):
    sigPoint = QtCore.pyqtSignal(np.ndarray, np.ndarray)
    sigError = QtCore.pyqtSignal(str)
    sigMoveMotor = QtCore.pyqtSignal(str, float)
    sigStopScan = QtCore.pyqtSignal(bool)
    sigShot = QtCore.pyqtSignal(str)
    sigFit = QtCore.pyqtSignal(np.ndarray, float)

    def __init__(self):
        super().__init__()
        self.scanTimer = QtCore.QTimer(self)
        self.scanTimer.setInterval(500)
        # noinspection PyUnresolvedReferences
        self.scanTimer.timeout.connect(self.checkScanFiles)
        self.params = {}
        self.running = False
        self.executor = concurrent.futures.ThreadPoolExecutor(1)
        self.future = self.executor.submit(lambda _: _)

    def setConfig(self, config):
        self.config = config

    def checkFiles(self):
        for pos, fn in self.readImages[:]:
            image = os.path.join(self.config.dataDir, fn)
            if not os.path.exists(image):
                continue
            cbf = cbfimage.CbfImage(image)
            cbf.array[cbf.array < 0] = 0
            roi = cbf.array.sum()
            self.scanY[np.where(self.scanX == pos)[0]] = roi
            self.sigPoint.emit(self.scanX, self.scanY)
            self.readImages.remove((pos, fn))
            os.remove(image)

    def checkScanFiles(self):
        if not self.running or self.future.running():
            return
        if self.readImages:
            self.future = self.executor.submit(self.checkFiles)
        else:
            self.scanTimer.stop()
            self.running = False
            if self.params['auto']:
                self.fit()
            self.sigStopScan.emit(self.params['auto'])

    def fit(self):
        x, y = self.scanX, self.scanY
        xc = (x * y).sum() / y.sum()
        w = np.sqrt(abs((y * (x - xc) ** 2).sum() / y.sum()))
        a = y.max()
        try:
            # noinspection PyTypeChecker
            res, cov = optimize.curve_fit(gauss, self.scanX, self.scanY, (xc, w, a))
        except RuntimeError as err:
            self.sigError.emit(f'Fit could not be done: {str(err)}')
            self.sigMoveMotor.emit(self.params['axis'], self.params['backup'])
            return
        fitfunc = gauss(x, *res)
        xc = res[0]
        self.sigFit.emit(fitfunc, xc)
        if xc > self.params['stop']:
            self.sigError.emit(f'The Gauss maximum is too right at {xc:.5f}, we move to {self.params["stop"]:.5f}')
            xc = self.params["stop"]
        elif xc < self.params['start']:
            self.sigError.emit(f'The Gauss maximum is too left at {xc:.5f}, we move to {self.params["start"]:.5f}')
            xc = self.params["start"]
        else:
            self.sigError.emit(f'The Gauss maximum is found to be at {xc:.5f}')
        self.sigMoveMotor.emit(self.scanAxis, xc)

    def run(self, params):
        self.params = params
        if self.params['auto']:
            self.params['start'] = self.params['backup'] - float(self.config.scanRange)
            self.params['stop'] = self.params['backup'] + float(self.config.scanRange)
            self.params['step'] = float(self.config.scanStep)
        self.scanX = np.arange(self.params['start'], self.params['stop'] + self.params['step'], self.params['step'])
        if not self.scanX.size:
            self.sigError.emit('Scan error: there are not points to scan, check the signs')
            self.sigStopScan.emit(self.params['auto'])
            return
        self.scanY = np.zeros_like(self.scanX)
        self.scanImages = [(float(p), f'{str(uuid.uuid4())}.cbf') for p in self.scanX][::-1]
        self.readImages = self.scanImages[:]
        self.running = True
        self.scanTimer.start()
        self.moveMotor()

    def moveMotor(self):
        if self.running and self.scanImages:
            self.position, self.imageName = self.scanImages.pop()
            self.sigMoveMotor.emit(self.params['axis'], self.position)

    def updateMotorPosition(self, name, position):
        if self.running and name == self.params['axis'] and abs(position - self.position) <= 1e-2 and self.imageName:
            name = self.imageName
            self.imageName = ''
            self.sigShot.emit(name)

    def abortScan(self):
        self.running = False
        self.scanTimer.stop()
        self.future.cancel()
        self.readImages = []
        self.scanImages = []
        if self.params['auto']:
            self.sigMoveMotor.emit(self.params['axis'], self.params['backup'])
        self.sigStopScan.emit(self.params['auto'])
