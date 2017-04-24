#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.ui_wblower import Ui_WBlower
from ..controller.config import Config


class WBlower(QtWidgets.QDialog, Ui_WBlower):
    sigClosed = QtCore.pyqtSignal()
    sigConnect = QtCore.pyqtSignal(str, str, str, str, str)
    sigDisconnect = QtCore.pyqtSignal()
    sigRun = QtCore.pyqtSignal(float, float)
    sigShowSeqAction = QtCore.pyqtSignal(dict, object)
    sigCreateSeqAction = QtCore.pyqtSignal(dict, object, bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.signalOnHold = None
        self.holdTemp = 0.
        self.temps = []
        self.runPlot = False
        self.paused = False
        self.setupUi(self)
        self.loadSettings()
        self.sigShowSeqAction.connect(self.showSeqAction)
        self.disconnectButton.hide()
        self.errorEdit.setValidator(QtGui.QDoubleValidator())

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def closeEvent(self, event):
        self.on_disconnectButton_clicked()
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()

    def saveSettings(self):
        s = Config.Settings
        s.setValue('WBlower/Geometry', self.saveGeometry())
        s.setValue('WBlower/target', self.targetSpinBox.value())
        s.setValue('WBlower/ramp', self.rampSpinBox.value())
        s.setValue('WBlower/host', self.hostEdit.text())
        s.setValue('WBlower/session', self.sessionEdit.text())
        s.setValue('WBlower/motor', self.motorEdit.text())
        s.setValue('WBlower/counter', self.counterEdit.text())
        s.setValue('WBlower/rampcmd', self.rampEdit.text())
        s.setValue('WBlower/error', self.errorEdit.text())

    def loadSettings(self):
        s = Config.Settings
        self.restoreGeometry(s.value('WBlower/Geometry', Config.QBA))
        self.targetSpinBox.setValue(float(s.value('WBlower/target', 25)))
        self.rampSpinBox.setValue(float(s.value('WBlower/ramp', 1)))
        self.hostEdit.setText(s.value('WBlower/host', 'snbla1.esrf.fr'))
        self.sessionEdit.setText(s.value('WBlower/session', 'rheuro'))
        self.motorEdit.setText(s.value('WBlower/motor', 'mblower'))
        self.counterEdit.setText(s.value('WBlower/counter', 'ceuro'))
        self.rampEdit.setText(s.value('WBlower/rampcmd', 'euro2400parameters unit=0 RampRate={:.2f}'))
        self.errorEdit.setText(s.value('WBlower/error', '0.2'))

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.resume()
        self.close()

    def updateTemperature(self, value):
        if self.runPlot:
            self.temps.append(value)
            self.plotView.plot(y=self.temps, pen='g', clear=True)
        self.tempLabel.setText(f'<html><head/><body><p>{value:.1f} &deg;C</p></body></html>')
        if not self.paused and self.signalOnHold and abs(value - self.holdTemp) <= float(self.errorEdit.text()):
            self.signalOnHold.emit()
            self.signalOnHold = None

    @QtCore.pyqtSlot()
    def on_runButton_clicked(self):
        self.runBlower(self.targetSpinBox.value(), self.rampSpinBox.value())

    def runBlower(self, target, ramp):
        self.resume()
        self.currentLabel.setText(f'<html><head/><body><p>{target:.1f} &deg;C | {ramp}&deg;C/min</p></body></html>')
        self.sigRun.emit(target, ramp)

    @QtCore.pyqtSlot()
    def on_toSeqButton_clicked(self):
        target = self.targetSpinBox.value()
        ramp = self.rampSpinBox.value()
        self.createAction(target, ramp, False)

    def createAction(self, target, ramp, now):
        d = {
            f'Eurotherm: to {target:.1f} C with the rate {ramp:.1f} deg/min':
                {
                    f'Target temperature: {target:.1f} C': f'targetSpinBox={target:.1f}',
                    f'Ramp rate: {ramp:.1f} deg/min': f'rampSpinBox={ramp:.1f}'
                }
        }
        self.targetSpinBox.setValue(target)
        self.rampSpinBox.setValue(ramp)
        self.sigCreateSeqAction.emit(d, self.sigShowSeqAction, now)

    def showSeqAction(self, action, signal):
        for v in list(action.values())[0].values():
            name, val = v.split('=')
            self.__dict__[name].setValue(float(val))
        if signal:
            self.holdTemp = self.targetSpinBox.value()
            self.on_runButton_clicked()
            signal.emit()

    def setSignalOnHold(self, action, signal):
        if signal:
            self.resume()
            self.euroAction = action
            # We have to wait because communication with blower takes at least 1 sec
            QtCore.QTimer.singleShot(int(Config.CommTimeout), lambda: setattr(self, 'signalOnHold', signal))

    @QtCore.pyqtSlot()
    def on_startPlotButton_clicked(self):
        if self.runPlot:
            self.runPlot = False
            self.startPlotButton.setText('Start')
            self.startPlotButton.setIcon(QtGui.QIcon(':/run'))
        else:
            self.runPlot = True
            self.startPlotButton.setText('Stop')
            self.startPlotButton.setIcon(QtGui.QIcon(':/stop'))

    @QtCore.pyqtSlot()
    def on_clearPlotButton_clicked(self):
        self.temps = []
        self.plotView.clear()

    @QtCore.pyqtSlot()
    def on_connectButton_clicked(self):
        self.resume()
        host = self.hostEdit.text()
        session = self.sessionEdit.text()
        motor = self.motorEdit.text()
        counter = self.counterEdit.text()
        cmd = self.rampEdit.text()
        if host and session and motor and counter and cmd:
            self.sigConnect.emit(host, session, motor, counter, cmd)

    @QtCore.pyqtSlot()
    def on_disconnectButton_clicked(self):
        self.sigDisconnect.emit()
        self.connectionFailed()

    def connectionSucceed(self):
        self.connectButton.hide()
        self.disconnectButton.show()

    def connectionFailed(self):
        self.connectButton.show()
        self.disconnectButton.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
