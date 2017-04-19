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

    def __init__(self):
        super().__init__()
        self._p = None
        self._i = None
        self._d = None
        self._setp = None
        self._mout = None
        self._range = None
        self._temp = 0
        self._heater = 0

    def _setStatus(self, temp, heater):
        self._temp = temp
        self._heater = heater

    def temp(self):
        return self._temp

    def heater(self):
        return self._heater

    def _setParams(self, p, i, d, mout, rnge, setp):
        self._p = p
        self._i = i
        self._d = d
        self._mout = mout
        self._range = rnge
        self._setp = setp

    @customable
    def set(self, setp=None, p=None, i=None, d=None, mout=None, rng=None, **kwargs):
        setp = setp or self._setp
        if setp is None and not 0 <= setp <= 1000:
            raise ValueError('The Lakeshore setp value must be between 0 and 1000 K')
        p = p or self._p
        if p is not None and not 0.1 <= p <= 1000:
            raise ValueError('The Lakeshore propotional value must be between 0.1 and 1000')
        i = i or self._i
        if i is not None and not 0.1 <= i <= 1000:
            raise ValueError('The Lakeshore integral value must be between 0.1 and 1000')
        d = d or self._d
        if d is not None and not 0 <= d <= 200:
            raise ValueError('The Lakeshore differential value must be between 0.1 and 1000')
        mout = mout or self._mout
        if mout is not None and not 0 <= mout <= 100:
            raise ValueError('The Lakeshore manual output value must be between 0.1 and 1000')
        rng = rng or self._range
        if isinstance(rng, str):
            try:
                rng = LDevice.heaterRange.index(rng)
            except ValueError:
                rng = -1
        if rng is not None and not 0 <= rng <= 3:
            raise ValueError('The Lakeshore range value must be between 0 and 3')
        self._sigSet.emit((setp, p, i, d, mout, rng), kwargs.get('now', False))

    def setpoint(self, point):
        self.set(setp=point)

    def setpid(self, p, i, d):
        self.set(p=p, i=i, d=d)

    def setmout(self, mout):
        self.set(mout=mout)

    def setrng(self, rng):
        self.set(rng=rng)

    @customable
    def wait(self, **kwargs):
        self._sigCreateSeqAction.emit({'Wait for the Lakeshore temperature': 'waitOnTemp=1'}, self._sigHoldFromSeq,
                                      kwargs.get('now', False))
