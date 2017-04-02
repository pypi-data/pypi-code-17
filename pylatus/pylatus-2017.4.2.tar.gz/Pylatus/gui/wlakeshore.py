#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from .ui.ui_wlakeshore import Ui_WLakeshore
from ..devices.lakeshore import Lakeshore


class WLakeshore(QtWidgets.QDialog, Ui_WLakeshore):
    sigClosed = QtCore.pyqtSignal()
    sigAction = QtCore.pyqtSignal()
    sigCreateSeqAction = QtCore.pyqtSignal(dict, object, bool)
    sigShowSeqAction = QtCore.pyqtSignal(dict, object)
    lakeshoreReachedFromSeqSignal = QtCore.pyqtSignal(dict, object)
    sigConnect = QtCore.pyqtSignal(str, str, str, int)
    sigUpdateParameters = QtCore.pyqtSignal()
    sigStop = QtCore.pyqtSignal()
    sigSetParameters = QtCore.pyqtSignal(float, float, float, float, int, float)
    sigSetOutput = QtCore.pyqtSignal(str)
    sigSetSensor = QtCore.pyqtSignal(str)
    DEFAULT_PORT = 7777

    def __init__(self, parent, settings):
        super().__init__(parent=parent)
        self.settings = settings
        self.setupUi(self)
        self.loadSettings()
        self.aList = []
        self.plotView.addLegend()
        self.plotView.plot(self.aList, pen='g', name='Temperature')
        self.sensor = 'A'
        self.loadSettings()
        self.stopButton.hide()
        self.connectSignals()
        self.holdTemp = 0
        self.signalOnHold = None
        self.heaterRange = Lakeshore.heaterRange

    def connectSignals(self):
        self.sigShowSeqAction.connect(self.showSeqAction)
        self.lakeshoreReachedFromSeqSignal.connect(self.setSignalOnHold)

    def closeEvent(self, event):
        self.hide()
        self.on_stopButton_clicked()
        self.saveSettings()
        self.sigClosed.emit()

    def saveSettings(self):
        s = self.settings
        s.setValue('WLakeshore/Geometry', self.saveGeometry())
        s.setValue('WLakeshore/ip', self.ipLineEdit.text())
        s.setValue('WLakeshore/sensor', self.sensorComboBox.currentText())
        s.setValue('WLakeshore/output', self.outputComboBox.currentText())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WLakeshore/Geometry', QtCore.QByteArray()))
        self.ipLineEdit.setText(s.value('WLakeshore/ip', ''))
        sensor = self.sensorComboBox.findText(s.value('WLakeshore/sensor'))
        if sensor == -1:
            sensor = 0
        self.sensorComboBox.setCurrentIndex(sensor)
        output = self.outputComboBox.findText(s.value('WLakeshore/output'))
        if output == -1:
            output = 0
        self.outputComboBox.setCurrentIndex(output)

    def updateTemp(self, sensor, heater):
        if self.startButton.isVisible():
            self.startButton.hide()
            self.stopButton.show()
        self.aLabel.setText(f'{self.sensor}: {sensor:.2f} K')
        self.bLabel.setText(f'H: {heater:.2f}%')
        self.aList.append(sensor)
        self.plotView.plot(self.aList, pen='g', clear=True)
        if self.signalOnHold and abs(self.holdTemp - sensor) <= 0.2:
            self.signalOnHold.emit()
            self.signalOnHold = None

    def updateParams(self, p, i, d, mout, rnge, setp):
        self.pSpinBox.setValue(p)
        self.iSpinBox.setValue(i)
        self.dSpinBox.setValue(d)
        self.moutSpinBox.setValue(mout)
        self.setpSpinBox.setValue(setp)
        self.rangeComboBox.setCurrentIndex(rnge)

    @QtCore.pyqtSlot()
    def on_startButton_clicked(self):
        host = self.ipLineEdit.text()
        output = self.outputComboBox.currentText()
        sensor = self.sensorComboBox.currentText()
        self.aList = []
        self.sigConnect.emit(output, sensor, host, self.DEFAULT_PORT)

    @QtCore.pyqtSlot()
    def on_stopButton_clicked(self):
        self.stopButton.hide()
        self.startButton.show()
        self.sigStop.emit()

    @QtCore.pyqtSlot()
    def on_sendButton_clicked(self):
        self.sigSetParameters.emit(*self.collectParams())

    @QtCore.pyqtSlot()
    def on_updateButton_clicked(self):
        self.sigUpdateParameters.emit()

    @QtCore.pyqtSlot()
    def on_clearButton_clicked(self):
        self.aList = []
        self.plotView.clear()

    @QtCore.pyqtSlot()
    def on_seqButton_clicked(self):
        self.setScriptParams(self.collectParams(), False)

    def collectParams(self):
        p = self.pSpinBox.value()
        i = self.iSpinBox.value()
        d = self.dSpinBox.value()
        mout = self.moutSpinBox.value()
        rnge = self.rangeComboBox.currentIndex()
        setp = self.setpSpinBox.value()
        return p, i, d, mout, rnge, setp

    def showSeqAction(self, action, signal):
        for v in list(action.values())[0].values():
            name, val = v.split('=')
            try:
                self.__dict__[name].setValue(float(val))
            except AttributeError:
                self.__dict__[name].setCurrentIndex(int(val))
        if signal:
            self.holdTemp = self.setpSpinBox.value()
            self.on_sendButton_clicked()
            signal.emit()

    def setSignalOnHold(self, action, signal):
        if signal:
            self.lakeshoreAction = action
            self.signalOnHold = signal

    def lakeshoreError(self, msg):
        QtWidgets.QMessageBox.critical(self, 'Lakeshore error', msg)
        self.on_stopButton_clicked()

    @QtCore.pyqtSlot(str)
    def on_outputComboBox_currentIndexChanged(self, output):
        self.sigSetOutput.emit(output)
        self.on_clearButton_clicked()
        self.output = output

    @QtCore.pyqtSlot(str)
    def on_sensorComboBox_currentIndexChanged(self, sensor):
        self.sigSetSensor.emit(sensor)
        self.on_clearButton_clicked()
        self.sensor = sensor

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)

    def setScriptParams(self, params, now):
        setp, p, i, d, mout, rnge = params
        if p is not None:
            self.pSpinBox.setValue(p)
        if i is not None:
            self.iSpinBox.setValue(i)
        if d is not None:
            self.dSpinBox.setValue(d)
        if setp is not None:
            self.setpSpinBox.setValue(setp)
        if rnge >= 0:
            self.rangeComboBox.setCurrentIndex(rnge)
        p, i, d, mout, rnge, setp = self.collectParams()
        action = {
            f'Lakeshore: to {setp:.1f} K': {
                f'Setpoint: {setp:.1f} K': f'setpSpinBox={setp:.1f}',
                f'P: {p:.1f}': f'pSpinBox={p:.1f}',
                f'I: {i:.1f}': f'iSpinBox={i:.1f}',
                f'D: {d:.1f}': f'dSpinBox={d:.1f}',
                f'Manual Output: {mout:.2f}%': f'moutSpinBox={mout:.2f}',
                f'Heater Range: {self.heaterRange[rnge]}': f'rangeComboBox={rnge:d}',
            }
        }
        self.sigCreateSeqAction.emit(action, self.sigShowSeqAction, now)
