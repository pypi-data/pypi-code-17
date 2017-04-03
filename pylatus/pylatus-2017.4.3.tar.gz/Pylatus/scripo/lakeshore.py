#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from ..controller.decorators import customable
from ..devices.lakeshore import Lakeshore as LDevice


specialWords = ['lakeshore.set', 'lakeshore.setpoint', 'lakeshore.setpid', 'lakeshore.setmout', 'lakeshore.setrng',
                'lakeshore.wait']


class Lakeshore(QtCore.QObject):
    _sigSet = QtCore.pyqtSignal(tuple, bool)
    _sigHoldFromSeq = QtCore.pyqtSignal(dict, object)
    _sigCreateSeqAction = QtCore.pyqtSignal(dict, object, bool)

    @customable
    def set(self, setp=None, p=None, i=None, d=None, mout=None, rng=None, **kwargs):
        if setp is not None and not 0 <= setp <= 1000:
            raise ValueError('The Lakeshore setp value must be between 0 and 1000 K')
        else:
            self._sigSetPoint.emit(setp)
        if p is not None:
            if not 0.1 <= p <= 1000:
                raise ValueError('The Lakeshore propotional value must be between 0.1 and 1000')
        if i is not None:
            if not 0.1 <= i <= 1000:
                raise ValueError('The Lakeshore integral value must be between 0.1 and 1000')
        if d is not None:
            if not 0 <= d <= 200:
                raise ValueError('The Lakeshore differential value must be between 0.1 and 1000')
        if mout is not None:
            if not 0 <= mout <= 100:
                raise ValueError('The Lakeshore manual output value must be between 0.1 and 1000')
        if isinstance(rng, str):
            try:
                rng = LDevice.heaterRange.index(rng)
            except ValueError:
                rng = -1
        if rng is not None:
            if not 0 <= rng <= 3:
                raise ValueError('The Lakeshore range value must be between 0 and 3')
        self._sigSet.emit((setp, p, i, d, mout, rng), kwargs.get('now', False))

    def setpoint(self, point):
        self.set(setp=point)

    def setpid(self, p, i, d):
        self.set(p, i, d)

    def setmout(self, mout):
        self.set(mout=mout)

    def setrng(self, rng):
        self.set(rng=rng)

    @customable
    def wait(self, **kwargs):
        self._sigCreateSeqAction.emit({'Wait for the Lakeshore temperature': 'waitOnTemp=1'}, self._sigHoldFromSeq,
                                      kwargs.get('now', False))
