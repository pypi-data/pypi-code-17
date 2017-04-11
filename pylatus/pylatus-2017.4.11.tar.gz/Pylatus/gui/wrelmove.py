#!/usr/bin/python
# -*- coding: utf-8 -*-

import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.ui_wrelmove import Ui_WRelMove
from .gutils import GUtils
from ..controller import decorators


class WRelMove(QtWidgets.QDialog, Ui_WRelMove):
    sigClosed = QtCore.pyqtSignal()
    sigMoveMotorRelative = QtCore.pyqtSignal(str, float)
    sigStopAllMotors = QtCore.pyqtSignal(str)
    sigUpdateMotorViews = QtCore.pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent=parent)
        self.settings = settings
        self.setupUi(self)
        self.motors = set()
        self.userMotors = set()
        self.labels = {}
        self.kappa = True
        self.config = None
        self.resizeToMinimum()

    def setConfig(self, config):
        self.config = config
        self.userMotors = {self.config.pldistf, self.config.plrot, self.config.pldistd, self.config.plvert,
                           self.config.prver, self.config.prhor}
        self.setOmegaPhi()

    def setMotors(self, motors):
        self.motors = set()
        for motor in motors:
            self.setMotor(motor)

    @decorators.split_motor_name
    def setMotor(self, name):
        self.motors.add(name)
        self.setKappa(self.kappa)

    @decorators.split_motor_name
    def removeMotor(self, name):
        self.motors.discard(name)
        self.setKappa(self.kappa)

    def setOmegaPhi(self):
        self.setKappa(True)

    def setPrphi(self):
        self.setKappa(False)

    def setKappa(self, isKappa):
        if not self.config:
            return
        self.kappa = isKappa
        kappa = {self.config.kappa, self.config.phi, self.config.omega}
        prphi = {self.config.prphi}
        if isKappa:
            self.userMotors |= kappa
            self.userMotors ^= prphi
        else:
            self.userMotors ^= kappa
            self.userMotors |= prphi
        self.appendMotors(self.motors & self.userMotors)

    def appendMotors(self, motors):
        self.motorsComboBox.clear()
        self.motorsComboBox.addItems(sorted(motors))
        self.motorsComboBox.setCurrentIndex(-1)

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()
        super().closeEvent(event)

    def saveSettings(self):
        s = self.settings
        s.setValue('WRelMove/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WRelMove/Geometry', QtCore.QByteArray()))

    @QtCore.pyqtSlot(str)
    def on_motorsComboBox_activated(self, motorName):
        if motorName not in self.motors:
            return
        self.motorsComboBox.clearEditText()
        self.createRelativeMotorView(motorName)

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        self.on_motorsComboBox_activated(self.motorsComboBox.currentText())

    @QtCore.pyqtSlot()
    def on_rootButton_clicked(self):
        if GUtils.askPass(self):
            self.appendMotors(self.motors)

    def createRelativeMotorView(self, motorName):
        if motorName in self.labels:
            return
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        self.labels[motorName] = label
        spinBox = QtWidgets.QDoubleSpinBox()
        spinBox.setDecimals(4)
        spinBox.setMaximum(10000)
        spinBox.setMinimum(-10000)
        spinBox.setSingleStep(0.1)
        spinBox.setValue(0)
        # noinspection PyUnresolvedReferences
        spinBox.editingFinished.connect(lambda: self.moveMotor(True, motorName, spinBox))

        runButton = QtWidgets.QToolButton()
        runButton.setIcon(QtGui.QIcon(':/run'))
        # noinspection PyUnresolvedReferences
        runButton.clicked.connect(lambda: self.moveMotor(False, motorName, spinBox))

        stopButton = QtWidgets.QToolButton()
        stopButton.setIcon(QtGui.QIcon(':/stop'))
        # noinspection PyUnresolvedReferences
        stopButton.clicked.connect(lambda: self.sigStopAllMotors.emit(motorName))

        delButton = QtWidgets.QToolButton()
        delButton.setIcon(QtGui.QIcon(':/del'))
        # noinspection PyUnresolvedReferences
        delButton.clicked.connect(lambda: self.removeRelativeMotorView(layout, motorName))

        layout.addWidget(label)
        layout.addWidget(spinBox)
        layout.addWidget(runButton)
        layout.addWidget(stopButton)
        layout.addWidget(delButton)
        self.verticalLayout.addLayout(layout)
        self.sigUpdateMotorViews.emit()

    def resizeToMinimum(self):
        QtCore.QTimer.singleShot(10, lambda: self.resize(0, 0))

    def removeRelativeMotorView(self, layout, name):
        for widget in [layout.itemAt(i).widget() for i in range(layout.count())]:
            sip.delete(widget)
        del self.labels[name]
        self.verticalLayout.removeItem(layout)
        self.resizeToMinimum()

    def moveMotor(self, checkFocus, name, spinBox):
        if checkFocus and not spinBox.hasFocus():
            return
        self.sigMoveMotorRelative.emit(name, spinBox.value())

    def updateMotorPosition(self, name, position):
        if name in self.labels:
            label = self.labels[name]
            label.setText(f'{name}: {position:.5f}')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
