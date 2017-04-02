#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from ..controller.decorators import customable


specialWords = ['musst.openShutter', 'musst.closeShutter', 'musst.trigChannel']


class Musst(QtCore.QObject):
    __openShutterSignal = QtCore.pyqtSignal()
    __openShutterFromSeqSignal = QtCore.pyqtSignal(dict, object)
    __closeShutterSignal = QtCore.pyqtSignal()
    __closeShutterFromSeqSignal = QtCore.pyqtSignal(dict, object)
    __trigChannelSignal = QtCore.pyqtSignal(int, float)
    __trigChannelFromSeqSignal = QtCore.pyqtSignal(dict, object)

    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.__trigChannelFromSeqSignal.connect(self.__trigChannelFromSeq)
        self.__closeShutterFromSeqSignal.connect(self.__closeShutterFromSeq)
        self.__openShutterFromSeqSignal.connect(self.__openShutterFromSeq)
        self.__closeShutterSignal.connect(self.__wmain.diffractometer.musst.closeShutter)
        self.__openShutterSignal.connect(self.__wmain.diffractometer.musst.openShutter)
        self.__trigChannelSignal.connect(self.__wmain.diffractometer.musst.trigChannel)

    @customable
    def openShutter(self, **kwargs):
        self.__wmain.wseq.appendActionToSeqList(
            {'Open shutter': 'musstOpenShutter=1'},
            self.__openShutterFromSeqSignal,
            kwargs.get('now', False)
        )

    @customable
    def closeShutter(self, **kwargs):
        self.__wmain.wseq.appendActionToSeqList({'Close shutter': 'musstCloseShutter=1'},
                                                self.__closeShutterFromSeqSignal, kwargs.get('now', False))

    @customable
    def trigChannel(self, channel, trigtime=0.1, **kwargs):
        if not 8 <= channel <= 15:
            raise ValueError('The MUSST channel musst be between 8 and 15')
        elif trigtime < 0.01:
            raise ValueError('The MUSST triggering time is to low')
        d = {'Trigger MUSST channel {:d} for {:.2f} '
             'seconds'.format(channel, trigtime): 'trigChannel={:d};trigtime={:.2f}'.format(channel, trigtime)}
        self.__wmain.wseq.appendActionToSeqList(d, self.__trigChannelFromSeqSignal, kwargs.get('now', False))

    def __trigChannelFromSeq(self, dct, signal):
        if signal:
            channel, trigtime = dct.values()[0].split(';')
            channel = int(channel.split('=')[1])
            trigtime = float(trigtime.split('=')[1])
            self.__trigChannelSignal.emit(channel, trigtime)
            signal.emit()

    # noinspection PyUnusedLocal
    def __closeShutterFromSeq(self, dct, signal):
        if signal:
            self.__closeShutterSignal.emit()
            signal.emit()

    # noinspection PyUnusedLocal
    def __openShutterFromSeq(self, dct, signal):
        if signal:
            self.__openShutterSignal.emit()
            signal.emit()
