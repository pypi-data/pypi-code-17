#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from PyQt5 import QtCore
from ..controller.decorators import customable


specialWords = ['diffractometer.scan', 'diffractometer.sleep', 'diffractometer.custom']


class Diffractometer(QtCore.QObject):
    __sigSleep = QtCore.pyqtSignal(dict, object)
    __sigSetScanType = QtCore.pyqtSignal(dict, object)
    __sigCustomAction = QtCore.pyqtSignal(dict, object)
    _sigCreateSeqScanAction = QtCore.pyqtSignal(dict)
    _sigCreateSeqAction = QtCore.pyqtSignal(dict, object, bool)
    _sigSetScanTypeInGUI = QtCore.pyqtSignal(str)
    _sigCreateSeqCustomAction = QtCore.pyqtSignal(dict, object)

    def __init__(self):
        super().__init__()
        self.__custom = {}
        self.__sigSleep.connect(self.__sleepFromSeq)
        self.__sigSetScanType.connect(self.__setScanTypeFromSeq)
        self.__sigCustomAction.connect(self.__runCustomActionFromSeq)
        self.__phiScan = False

    def _setPhiScan(self):
        self.__phiScan = True

    def _setOmegaScan(self):
        self.__phiScan = False

    @customable
    def scan(self, **kwargs):
        # if we have a phi scan, then we should swap phi and omega values
        if self.__phiScan:
            omega = kwargs.get('omega', None)
            phi = kwargs.get('phi', None)
            if omega is not None:
                kwargs['phi'] = omega
                if phi is None:
                    del kwargs['omega']
            if phi is not None:
                kwargs['omega'] = phi
                if omega is None:
                    del kwargs['phi']
        self._sigCreateSeqScanAction.emit(kwargs)

    @customable
    def setPhiScan(self, **kwargs):
        self._sigCreateSeqAction.emit({'Set PHI scan': 'scan=phi'}, self.__sigSetScanType, kwargs.get('now', False))

    @customable
    def setOmegaScan(self, **kwargs):
        self._sigCreateSeqAction.emit({'Set OMEGA scan': 'scan=omega'}, self.__sigSetScanType, kwargs.get('now', False))

    @customable
    def sleep(self, sec, **kwargs):
        sec = float(sec)
        if sec < 0:
            raise ValueError('Sleep time cannot be less than 0')
        self._sigCreateSeqAction.emit({f'Sleep for {sec:.3f} sec': f'sleep={sec:.3f}'}, self.__sigSleep,
                                      kwargs.get('now', False))

    def __sleepFromSeq(self, action, signal):
        if signal:
            sleepTime = float(list(action.values())[0].split('=')[1])
            QtCore.QTimer.singleShot(int(sleepTime * 1e3), signal.emit)

    def __setScanTypeFromSeq(self, action, signal):
        if signal:
            self._sigSetScanTypeInGUI.emit(list(action.values())[0].split('=')[1])
            signal.emit()

    def custom(self, useraction):
        t = str(time.time())
        self.__custom[t] = useraction
        self._sigCreateSeqAction.emit({f'Run custom action: {useraction.__name__}': f'action={t}'},
                                      self.__sigCustomAction, False)

    def __runCustomActionFromSeq(self, action, signal):
        if signal:
            self.__custom.pop(list(action.values())[0].split('=')[1], lambda: None)()
            signal.emit()
