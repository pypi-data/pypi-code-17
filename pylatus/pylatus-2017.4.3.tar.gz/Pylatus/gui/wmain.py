#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sip
from PyQt5 import QtCore, QtGui, QtWidgets
from ..devices import logger
from .ui.ui_wmain import Ui_WPylatus
from .wabout import WAbout
from .gutils import GUtils
from ..controller.utils import pyqt2bool as p2b


class WMain(QtWidgets.QMainWindow, Ui_WPylatus):
    sigClose = QtCore.pyqtSignal()
    sigConnectMotor = QtCore.pyqtSignal(str, str, str)
    sigRemoveMotor = QtCore.pyqtSignal(str)
    sigStopAllMotors = QtCore.pyqtSignal()
    sigConnectDetector = QtCore.pyqtSignal()
    sigReconnectMotors = QtCore.pyqtSignal()
    sigAbort = QtCore.pyqtSignal()
    sigUpdateWavelength = QtCore.pyqtSignal(float)
    sigSetMinPlvert = QtCore.pyqtSignal(float)
    sigSetPhiScan = QtCore.pyqtSignal()
    sigSetOmegaScan = QtCore.pyqtSignal()
    sigSetPrphiScan = QtCore.pyqtSignal()
    sigStartExperiment = QtCore.pyqtSignal(dict)
    sigCreateSeqAction = QtCore.pyqtSignal(dict, object)
    sigShowSeqAction = QtCore.pyqtSignal(dict, object)

    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.setupUi(self)
        self.sigSeqDone = None
        self.actionHideMainWindow.setChecked(not sys.platform.startswith('linux'))
        self.motorsList.keyPressEvent = self.motorsListKeyPressEvent
        self.logger = logger.Logger('GUI')
        self.running = False
        self.sigShowSeqAction.connect(self.showSequenceAction)

    def showLamp(self, show):
        self.lampLabel.setVisible(show)
        self.lampTextLabel.setVisible(show)

    def changeLampColor(self, noCounts):
        self.lampLabel.setPixmap(QtGui.QPixmap(':/rlamp' if noCounts else ':/lamp'))

    def closeEvent(self, event):
        self.saveSettings()
        self.sigClose.emit()

    def saveSettings(self):
        s = self.settings
        s.setValue('WMain/Geometry', self.saveGeometry())
        s.setValue('WMain/filename', self.filenameLineEdit.text())
        s.setValue('WMain/exposition', self.exposureSpinBox.value())
        s.setValue('WMain/nframes', self.nframesSpinBox.value())
        s.setValue('WMain/dOmega', self.dOmegaSpinBox.value())
        s.setValue('WMain/sOmega', self.omegaSpinBox.value())
        s.setValue('WMain/phi', self.phiSpinBox.value())
        s.setValue('WMain/kappa', self.kappaSpinBox.value())
        s.setValue('WMain/folder', self.folderLineEdit.text())
        s.setValue('WMain/isKappa', self.kappaCheckBox.isChecked())
        s.setValue('WMain/phiScan', self.phiScanCheckBox.isChecked())
        s.setValue('WMain/pauseExp', self.pauseBeamOffCheckBox.isChecked())
        s.setValue('WMain/nperiods', self.nperiodsSpinBox.value())
        s.setValue('WMain/pldistd', self.pldistdSpinBox.value())
        s.setValue('WMain/pldistf', self.pldistfSpinBox.value())
        s.setValue('WMain/plrot', self.plrotSpinBox.value())
        s.setValue('WMain/plvert', self.plvertSpinBox.value())
        s.setValue('WMain/mod', self.modSpinBox.value())
        s.setValue('WMain/mod2', self.mod2SpinBox.value())
        s.setValue('WMain/zeroDist', self.zeroSpinBox.value())
        s.setValue('WMain/beamx', self.beamxSpinBox.value())
        s.setValue('WMain/beamy', self.beamySpinBox.value())
        s.setValue('WMain/detx', self.detectorxSpinBox.value())
        s.setValue('WMain/dety', self.detectorySpinBox.value())
        s.setValue('WMain/pixx', self.pixelxSpinBox.value())
        s.setValue('WMain/pixy', self.pixelySpinBox.value())
        s.setValue('WMain/prphiMax', self.prphiMaxSpinBox.value())
        s.setValue('WMain/phiMax', self.phiMaxSpinBox.value())
        s.setValue('WMain/omegaMax', self.omegaMaxSpinBox.value())
        s.setValue('WMain/wavelength', self.wlSpinBox.value())
        s.setValue('WMain/minplvert', self.minPlvertSpinBox.value())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WMain/Geometry', QtCore.QByteArray()))
        self.filenameLineEdit.setText(s.value('WMain/filename', ''))
        self.exposureSpinBox.setValue(float(s.value('WMain/exposition', 0)))
        self.nframesSpinBox.setValue(int(s.value('WMain/nframes', 1)))
        self.dOmegaSpinBox.setValue(float(s.value('WMain/dOmega', 0)))
        self.omegaSpinBox.setValue(float(s.value('WMain/sOmega', 0)))
        self.phiSpinBox.setValue(float(s.value('WMain/phi', 0)))
        self.kappaSpinBox.setValue(float(s.value('WMain/kappa', 0)))
        self.folderLineEdit.setText(s.value('WMain/folder', ''))
        self.kappaCheckBox.setChecked(p2b(s.value('WMain/isKappa', True)))
        self.phiScanCheckBox.setChecked(p2b(s.value('WMain/phiScan', False)))
        self.nperiodsSpinBox.setValue(int(s.value('WMain/nperiods', 1)))
        self.pldistdSpinBox.setValue(float(s.value('WMain/pldistd', 0)))
        self.pldistfSpinBox.setValue(float(s.value('WMain/pldistf', 0)))
        self.plrotSpinBox.setValue(float(s.value('WMain/plrot', 0)))
        self.plvertSpinBox.setValue(float(s.value('WMain/plvert', 0)))
        self.modSpinBox.setValue(int(s.value('WMain/mod', 0)))
        self.mod2SpinBox.setValue(int(s.value('WMain/mod2', 0)))
        self.zeroSpinBox.setValue(float(s.value('WMain/zeroDist', 156.88)))
        self.beamxSpinBox.setValue(float(s.value('WMain/beamx', 542.414)))
        self.beamySpinBox.setValue(float(s.value('WMain/beamy', 732.4)))
        self.detectorxSpinBox.setValue(int(s.value('WMain/detx', 1679)))
        self.detectorySpinBox.setValue(int(s.value('WMain/dety', 1475)))
        self.pixelxSpinBox.setValue(float(s.value('WMain/pixx', 172)))
        self.pixelySpinBox.setValue(float(s.value('WMain/pixy', 172)))
        self.prphiMaxSpinBox.setValue(float(s.value('WMain/prphiMax', 10)))
        self.phiMaxSpinBox.setValue(float(s.value('WMain/phiMax', 10)))
        self.omegaMaxSpinBox.setValue(float(s.value('WMain/omegaMax', 10)))
        self.wlSpinBox.setValue(float(s.value('WMain/wavelength', 0.69)))
        self.minPlvertSpinBox.setValue(float(s.value('WMain/minplvert', -20)))
        self.pauseBeamOffCheckBox.setChecked(p2b(s.value('WMain/pauseExp', False)))

    @QtCore.pyqtSlot(bool)
    def on_actionHideMainWindow_toggled(self, checked):
        self.tabWidget.setHidden(checked)
        self.statusbar.setHidden(checked)
        QtCore.QTimer.singleShot(10, lambda: self.resize(0, 0))

    @QtCore.pyqtSlot()
    def on_actionStopMotors_toggled(self):
        self.sigStopAllMotors.emit()

    def experimentFinished(self):
        self.running = False
        self.showLamp(False)
        self.statusbar.showMessage('Experiment has been finished')
        if self.sigSeqDone:
            signal = self.sigSeqDone
            self.sigSeqDone = None
            signal.emit()

    def experimentStarted(self):
        self.running = True
        self.showLamp(True)
        self.statusbar.showMessage('Experiment has been started')

    @QtCore.pyqtSlot()
    def on_measureButton_clicked(self):
        cbfBaseName = self.filenameLineEdit.text()
        if not cbfBaseName:
            self.logger.error('Give the base file name!')
            return
        if cbfBaseName.endswith('.cbf'):
            cbfBaseName = cbfBaseName[:-4]
            self.filenameLineEdit.setText(cbfBaseName)
        userSubDir = self.folderLineEdit.text()
        if not userSubDir:
            self.logger.error('Choose the data folder!')
            return
        params = {
            'periods': self.nperiodsSpinBox.value(),
            'cbfBaseName': cbfBaseName,
            'userSubDir': userSubDir,
            'nframes': self.nframesSpinBox.value(),
            'expPeriod': self.exposureSpinBox.value(),
            'startAngle': self.omegaSpinBox.value(),
            'step': self.dOmegaSpinBox.value(),
            'omegaphi': self.phiSpinBox.value(),
            'kappa': self.kappaSpinBox.value(),
            'mod': self.modSpinBox.value(),
            'mod2': self.mod2SpinBox.value(),
            'zeroDistance': self.zeroSpinBox.value(),
            'beamX': self.beamxSpinBox.value(),
            'beamY': self.beamySpinBox.value(),
            'pixelX': self.pixelxSpinBox.value(),
            'pldistf': self.pldistfSpinBox.value(),
            'pldistd': self.pldistdSpinBox.value(),
            'plvert': self.plvertSpinBox.value(),
            'plrot': self.plrotSpinBox.value(),
        }
        self.sigStartExperiment.emit(params)

    @QtCore.pyqtSlot()
    def on_actionConnectToPilatus_triggered(self):
        self.sigConnectDetector.emit()

    @QtCore.pyqtSlot()
    def on_actionConnectToMotors_triggered(self):
        self.sigReconnectMotors.emit()

    def showDCTime(self, days, hours, minutes, totalMin):
        self.expTime = totalMin
        if days and hours:
            t = f'{days:d}d {hours:d}h {minutes:d}m'
        elif hours:
            t = f'{hours:d}h {minutes:d}m'
        else:
            t = f'{minutes:d}m'
        self.timeLabel.setText(t)

    def showMax2Theta(self, angle, d):
        self.max2ThetaLabel.setText(f'<html><body>{angle:.1f}&deg;|{d:.3f} &Aring;' '</body></html>')

    @QtCore.pyqtSlot()
    def on_selectFolderButton_clicked(self):
        txt = self.folderLineEdit.text()
        if txt.startswith('/'):
            txt = txt[1:]
        dirr = os.path.join(self.config.userDir, txt)
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder for the data', dirr)
        if not folder:
            return
        elif not folder.startswith(self.config.userDir):
            QtWidgets.QMessageBox.critical(self, 'Wrong parent folder',
                                           f'The chosen folder must be within {self.config.userDir}')
            return
        dataDir = folder[len(self.config.userDir)+1:]
        self.folderLineEdit.setText(dataDir)

    @QtCore.pyqtSlot()
    def on_abortButton_clicked(self):
        self.sigAbort.emit()

    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QtWidgets.QMessageBox.aboutQt(self)

    @QtCore.pyqtSlot()
    def on_actionAboutPylatus_triggered(self):
        WAbout(self).exec()

    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_addSeqButton_clicked(self):
        aw = {}
        for labelName in self.__dict__:
            label = self.__dict__[labelName]
            if not isinstance(label, QtWidgets.QLabel) or not label.isEnabled():
                continue
            buddy = label.buddy()
            if buddy is not None:
                value = buddy.text()
                labelText = re.sub(r'<[^>]*>', '', label.text())
                aw[f'{labelText}: {value}'] = f'{buddy.objectName()}={value}'
        self.sigCreateSeqAction.emit({f'Data collection for {self.expTime:.1f} min': aw}, self.sigShowSeqAction)

    def showSequenceAction(self, action, signal):
        for elem in list(action.values())[0].values():
            widgetName, value = elem.split('=')
            widget = self.__dict__[widgetName]
            if isinstance(widget, QtWidgets.QSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                widget.setValue(float(value))
            elif isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(value)
        if signal:
            self.sigSeqDone = signal
            self.on_measureButton_clicked()

    @QtCore.pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        self.kappaGroupBox.setDisabled(True)
        self.musstGroupBox.setDisabled(True)
        self.beamGroupBox.setDisabled(True)
        self.detectorGroupBox.setDisabled(True)
        self.devicesGroupBox.setDisabled(True)
        self.prphiMaxSpinBox.setDisabled(True)
        self.phiMaxSpinBox.setDisabled(True)
        self.omegaMaxSpinBox.setDisabled(True)
        self.minPlvertSpinBox.setDisabled(True)
        self.settingsButton.setDisabled(True)
        if index == 1 and GUtils.askPass(self):
            self.kappaGroupBox.setEnabled(True)
            self.musstGroupBox.setEnabled(True)
            self.beamGroupBox.setEnabled(True)
            self.detectorGroupBox.setEnabled(True)
            self.pauseBeamOffCheckBox.setEnabled(not self.running)
        elif index == 2 and GUtils.askPass(self):
            self.devicesGroupBox.setEnabled(True)
            self.prphiMaxSpinBox.setEnabled(True)
            self.phiMaxSpinBox.setEnabled(True)
            self.omegaMaxSpinBox.setEnabled(True)
            self.minPlvertSpinBox.setEnabled(True)
            self.settingsButton.setEnabled(True)
        self.saveSettings()

    @QtCore.pyqtSlot(bool)
    def on_kappaCheckBox_toggled(self, checked):
        self.phiSpinBox.setEnabled(checked)
        self.phiLabel.setEnabled(checked)
        self.kappaSpinBox.setEnabled(checked)
        self.kappaLabel.setEnabled(checked)
        self.phiScanCheckBox.setEnabled(checked)
        self.phiScanCheckBox.setChecked(False)
        if checked:
            self.sigSetOmegaScan.emit()
        else:
            self.sigSetPrphiScan.emit()

    @QtCore.pyqtSlot(bool)
    def on_phiScanCheckBox_toggled(self, checked):
        an1, an2 = ('&phi;', '&omega;') if checked else ('&omega;', '&phi;')
        self.dAngleLabel.setText(f'<html><head/><body><p>&Delta;{an1} per image (deg)</p></body></html>')
        self.startingAngleLabel.setText(f'<html><head/><body><p>Starting {an1}<span style="vertical-align:sub;">0'
                                        f'</span> (deg)</p></body></html>')
        self.phiLabel.setText(f'<html><head/><body><p>Position of {an2} (deg)</p></body></html>')
        if checked:
            self.sigSetPhiScan.emit()
        else:
            self.sigSetOmegaScan.emit()

    def runFromScript(self, args):
        for labelName in self.__dict__:
            label = self.__dict__[labelName]
            if not isinstance(label, QtWidgets.QLabel) or not label.isEnabled():
                continue
            control = label.buddy()
            if control is None:
                continue
            controlName = control.objectName()
            for argName in args:
                if argName in controlName:
                    if isinstance(control, QtWidgets.QSpinBox):
                        control.setValue(int(args[argName]))
                    elif isinstance(control, QtWidgets.QDoubleSpinBox):
                        control.setValue(float(args[argName]))
                    elif isinstance(control, QtWidgets.QLineEdit):
                        control.setText(args[argName])
        self.on_addSeqButton_clicked()

    @QtCore.pyqtSlot()
    def on_addDeviceButton_clicked(self):
        host = self.specServerLineEdit.text()
        spec = self.specSessionLineEdit.text()
        motor = self.specMotorLineEdit.text()
        self.sigConnectMotor.emit(host, spec, motor)

    def motorsListKeyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            for item in self.motorsList.selectedItems():
                self.sigRemoveMotor.emit(item.text())
                sip.delete(item)
        else:
            QtWidgets.QListWidget.keyPressEvent(self.motorsList, event)

    @QtCore.pyqtSlot(float)
    def on_minPlvertSpinBox_valueChanged(self, value):
        self.plvertSpinBox.setMinimum(value)
        self.sigSetMinPlvert.emit(value)

    @QtCore.pyqtSlot()
    def on_updateButton_clicked(self):
        self.sigUpdateWavelength.emit(self.wlSpinBox.value())

    def showMotorsList(self, motors):
        self.motorsList.insertItems(0, motors)

    def showMotor(self, motor):
        self.motorsList.insertItem(0, motor)

    def showEvent(self, event):
        super().showEvent(event)
        self.on_tabWidget_currentChanged(0)
        self.experimentFinished()

    def setConfig(self, config):
        self.config = config

    def showTimeLeft(self, message):
        self.lampTextLabel.setText(message)

    def setScanType(self, scanType):
        if self.kappaCheckBox.isChecked():
            if scanType == 'omega':
                self.phiScanCheckBox.setChecked(False)
            elif scanType == 'phi':
                self.phiScanCheckBox.setChecked(True)
