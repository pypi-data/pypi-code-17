#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import json
from PyQt5 import QtCore
from ..gui import wmain, wlogging, wstatus, wuserstatus, wrelmove, walign
from ..gui import wscripted, wscan, wlakeshore, wblower, wcryo, wseq, woptions
from ..gui.gutils import GUtils
from ..devices import logger, diffractometer
from .. import scripo
from . import utils


class Controller(QtCore.QObject):
    sigConnectMotors = QtCore.pyqtSignal(list)
    sigConnectMotor = QtCore.pyqtSignal(str)
    sigMax2Theta = QtCore.pyqtSignal(float, float)
    sigDCTime = QtCore.pyqtSignal(int, int, int, float)
    sigExpTimeLeft = QtCore.pyqtSignal(str)
    sigScriptError = QtCore.pyqtSignal(str)
    sigGUIStarted = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.started = False
        self.createObjects()
        self.createScripo()
        self.createWindows()
        self.createDiffractometer()
        self.connectSignals()

    def createScripo(self):
        self.scipts = {
            'diffractometer': scripo.Diffractometer(),
            'blower': scripo.Blower(),
            'cryostream': scripo.Cryostream(),
            'lakeshore': scripo.Lakeshore(),
            'motor': scripo.Motor(),
        }

    def createObjects(self):
        self.motors = []
        self.expTime = 0
        self.expStarted = 0
        self.expPaused = 0
        self.wavelength = None
        self.energy = None
        self.expTimer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.expTimer.timeout.connect(self.calcExpTime)
        self.expTimer.setInterval(1000)

    def createWindows(self):
        self.settings = QtCore.QSettings()
        self.wmain = wmain.WMain(self.settings)
        self.wlogging = wlogging.WLogging(self.wmain, self.settings)
        self.wstatus = wstatus.WStatus(self.wmain, self.settings)
        self.wuserstatus = wuserstatus.WUserStatus(self.wmain, self.settings)
        self.wrelmove = wrelmove.WRelMove(self.wmain, self.settings)
        self.walign = walign.WAlign(self.wmain, self.settings)
        self.wscan = wscan.WScan(self.wmain, self.settings)
        self.wlakeshore = wlakeshore.WLakeshore(self.wmain, self.settings)
        self.wblower = wblower.WBlower(self.wmain, self.settings)
        self.wcryo = wcryo.WCryo(self.wmain, self.settings)
        self.wseq = wseq.WSeq(self.wmain, self.settings)
        self.wscripted = wscripted.WScriptEd(self.wmain, self.settings, self.scipts)
        self.woptions = woptions.WOptions(self.wmain, self.settings)
        self.logger = logger.Logger('GUI')

    def connectSignals(self):
        self.connectConfigSignals()
        self.connectActionSignals()
        self.connectMotorSignals()
        self.connectGUISignals()
        self.connectLoggingSignals()
        self.connectDiffractometerSignals()
        self.connectBlowerSignals()
        self.connectCryoSignals()
        self.connectScanSignals()
        self.connectLakeshoreSignals()
        self.connectSequenceSignals()

    def connectConfigSignals(self):
        self.woptions.sigConfig.connect(GUtils.setConfig)
        self.woptions.sigConfig.connect(self.wmain.setConfig)
        self.woptions.sigConfig.connect(self.wuserstatus.setConfig)
        self.woptions.sigConfig.connect(self.wscan.setConfig)
        self.woptions.sigConfig.connect(self.wcryo.setConfig)
        self.woptions.sigConfig.connect(self.wstatus.setConfig)
        self.woptions.sigConfig.connect(self.walign.setConfig)
        self.woptions.sigConfig.connect(self.wlogging.setConfig)
        self.woptions.sigConfig.connect(self.wseq.setConfig)
        self.woptions.sigConfig.connect(self.wrelmove.setConfig)
        self.woptions.sigConfig.connect(self.diffractometer.setConfig)
        self.woptions.sigConfig.connect(self.continueStart)

    def connectActionSignals(self):
        self.wmain.sigClose.connect(self.stop)
        self.wmain.actionLogging.toggled[bool].connect(self.wlogging.setVisible)
        self.wlogging.sigClosed.connect(lambda: self.wmain.actionLogging.setChecked(False))
        self.wstatus.sigClosed.connect(lambda: self.wmain.actionStatus.setChecked(False))
        self.wmain.actionStatus.toggled[bool].connect(self.showStatusWindow)
        self.wuserstatus.sigClosed.connect(lambda: self.wmain.actionUserStatus.setChecked(False))
        self.wuserstatus.sigShowRelativeWindow.connect(self.wmain.actionRelMove.trigger)
        self.wmain.actionUserStatus.toggled[bool].connect(self.wuserstatus.setVisible)
        self.wrelmove.sigClosed.connect(lambda: self.wmain.actionRelMove.setChecked(False))
        self.wmain.actionRelMove.toggled[bool].connect(self.wrelmove.setVisible)
        self.walign.sigClosed.connect(lambda: self.wmain.actionAlignment.setChecked(False))
        self.wmain.actionAlignment.toggled[bool].connect(self.showAlignWindow)
        self.wscan.sigClosed.connect(lambda: self.wmain.actionGeneralScan.setChecked(False))
        self.wmain.actionGeneralScan.toggled[bool].connect(self.wscan.setVisible)
        self.wlakeshore.sigClosed.connect(lambda: self.wmain.actionLakeshore.setChecked(False))
        self.wmain.actionLakeshore.toggled[bool].connect(self.wlakeshore.setVisible)
        self.wblower.sigClosed.connect(lambda: self.wmain.actionBlower.setChecked(False))
        self.wmain.actionBlower.toggled[bool].connect(self.wblower.setVisible)
        self.wcryo.sigClosed.connect(lambda: self.wmain.actionCryostream.setChecked(False))
        self.wmain.actionCryostream.toggled[bool].connect(self.wcryo.setVisible)
        self.wseq.sigClosed.connect(lambda: self.wmain.actionSequence.setChecked(False))
        self.wmain.actionSequence.toggled[bool].connect(self.wseq.setVisible)
        self.wscripted.sigClosed.connect(lambda: self.wmain.actionScriptEditor.setChecked(False))
        self.wmain.actionScriptEditor.toggled[bool].connect(self.wscripted.setVisible)
        self.wmain.settingsButton.clicked.connect(self.woptions.exec)

    def connectMotorSignals(self):
        self.wmain.sigReconnectMotors.connect(self.diffractometer.connectSpec)
        self.sigConnectMotors.connect(self.diffractometer.setMotors)
        self.sigConnectMotors.connect(self.wmain.showMotorsList)
        self.sigConnectMotors.connect(self.wrelmove.setMotors)
        self.sigConnectMotors.connect(self.wscan.addMotors)
        self.sigConnectMotors.connect(self.scipts['motor']._addMotors)
        self.wmain.sigConnectMotor.connect(self.addMotor)
        self.sigConnectMotor.connect(self.wmain.showMotor)
        self.sigConnectMotor.connect(self.diffractometer.connectGUIMotor)
        self.sigConnectMotor.connect(self.wrelmove.setMotor)
        self.sigConnectMotor.connect(self.wscan.addMotor)
        self.sigConnectMotor.connect(self.scipts['motor']._addMotor)
        self.wmain.sigRemoveMotor.connect(self.removeMotor)
        self.wmain.sigRemoveMotor.connect(self.diffractometer.deleteMotor)
        self.wmain.sigRemoveMotor.connect(self.wrelmove.removeMotor)
        self.wmain.sigRemoveMotor.connect(self.wscan.removeMotor)
        self.wmain.sigRemoveMotor.connect(self.scipts['motor']._removeMotor)
        self.diffractometer.sigWavelength.connect(self.setWavelength)
        self.diffractometer.sigWavelength.connect(self.wuserstatus.setWavelength)
        self.diffractometer.sigMotorMoved.connect(self.wuserstatus.updateMotorPosition)
        self.diffractometer.sigMotorMoved.connect(self.wstatus.updateMotorPosition)
        self.diffractometer.sigMotorMoved.connect(self.walign.updateMotorPosition)
        self.diffractometer.sigMotorMoved.connect(self.wrelmove.updateMotorPosition)
        self.diffractometer.sigMotorMoved.connect(self.wscan.updateMotorPosition)
        self.wrelmove.sigUpdateMotorViews.connect(self.diffractometer.updateMotorViews)
        self.wuserstatus.sigUpdateMotorViews.connect(self.diffractometer.updateMotorViews)
        self.wscan.sigUpdateMotorViews.connect(self.diffractometer.updateMotorViews)
        self.wrelmove.sigMoveMotorRelative.connect(self.diffractometer.moveMotorRelative)
        self.wrelmove.sigStopAllMotors.connect(self.diffractometer.stopAllMotors)
        self.wuserstatus.sigStopAllMotors.connect(self.diffractometer.stopAllMotors)
        self.wstatus.sigStopAllMotors.connect(self.diffractometer.stopAllMotors)
        self.walign.sigStopAllMotors.connect(self.diffractometer.stopAllMotors)
        self.wuserstatus.sigMoveMotor.connect(self.diffractometer.moveMotor)
        self.wstatus.sigMoveMotor.connect(self.diffractometer.moveMotor)
        self.walign.sigMoveMotor.connect(self.diffractometer.moveMotor)
        self.wmain.sigUpdateWavelength.connect(self.diffractometer.updateWavelength)
        self.diffractometer.sigAllMotorsStopped.connect(self.scipts['motor']._allMotorsStopped)

    def connectGUISignals(self):
        self.sigGUIStarted.connect(self.diffractometer.pilatus.setGuiStarted)
        self.sigMax2Theta.connect(self.wmain.showMax2Theta)
        self.wmain.pixelxSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.beamxSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.detectorxSpinBox.valueChanged[int].connect(self.calcMax2Theta)
        self.wmain.plvertSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.pldistdSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.zeroSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.pldistfSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.plrotSpinBox.valueChanged[float].connect(self.calcMax2Theta)
        self.wmain.exposureSpinBox.valueChanged[float].connect(self.calcDCTime)
        self.wmain.nframesSpinBox.valueChanged[int].connect(self.calcDCTime)
        self.wmain.nperiodsSpinBox.valueChanged[int].connect(self.calcDCTime)
        self.sigDCTime.connect(self.wmain.showDCTime)
        self.wmain.pauseBeamOffCheckBox.toggled[bool].connect(self.diffractometer.setMakePause)
        self.wmain.sigSetMinPlvert.connect(self.diffractometer.setMinPlvert)
        self.wmain.omegaMaxSpinBox.valueChanged[float].connect(self.diffractometer.setOmegaMaxVelocity)
        self.wmain.phiMaxSpinBox.valueChanged[float].connect(self.diffractometer.setPhiMaxVelocity)
        self.wmain.prphiMaxSpinBox.valueChanged[float].connect(self.diffractometer.setPrphiMaxVelocity)
        self.wmain.sigSetPhiScan.connect(self.diffractometer.setPhiScan)
        self.wmain.sigSetPhiScan.connect(self.wuserstatus.setOmegaPhi)
        self.wmain.sigSetPhiScan.connect(self.wrelmove.setOmegaPhi)
        self.wmain.sigSetPhiScan.connect(self.scipts['diffractometer']._setPhiScan)
        self.wmain.sigSetOmegaScan.connect(self.diffractometer.setOmegaScan)
        self.wmain.sigSetOmegaScan.connect(self.wuserstatus.setOmegaPhi)
        self.wmain.sigSetOmegaScan.connect(self.wrelmove.setOmegaPhi)
        self.wmain.sigSetOmegaScan.connect(self.scipts['diffractometer']._setOmegaScan)
        self.wmain.sigSetPrphiScan.connect(self.diffractometer.setPrphiScan)
        self.wmain.sigSetPrphiScan.connect(self.wuserstatus.setPrphi)
        self.wmain.sigSetPrphiScan.connect(self.wrelmove.setPrphi)
        self.wmain.sigSetPrphiScan.connect(self.scipts['diffractometer']._setOmegaScan)
        self.wmain.sigConnectDetector.connect(self.diffractometer.pilatus.connectDetector)
        self.wmain.sigStartExperiment.connect(self.diffractometer.startExperiment)
        self.wmain.sigStartExperiment.connect(self.setExperimentTime)
        self.sigExpTimeLeft.connect(self.wmain.showTimeLeft)

    def connectLoggingSignals(self):
        self.logger.sigPostLogMessage.connect(self.wlogging.postLogMessage)
        self.wmain.logger.sigPostLogMessage.connect(self.wlogging.postLogMessage)
        self.diffractometer.logger.sigPostLogMessage.connect(self.wlogging.postLogMessage)
        self.diffractometer.pilatus.logger.sigPostLogMessage.connect(self.wlogging.postLogMessage)

    def connectDiffractometerSignals(self):
        self.diffractometer.sigExperimentResumed.connect(self.setExperimentTime)
        self.diffractometer.sigExperimentFinished.connect(self.wmain.experimentFinished)
        self.diffractometer.sigExperimentFinished.connect(self.expTimer.stop)
        self.diffractometer.sigExperimentStarted.connect(self.expTimer.start)
        self.diffractometer.sigExperimentStarted.connect(self.wmain.experimentStarted)
        self.wmain.sigAbort.connect(self.diffractometer.abortExperiment)
        self.diffractometer.monitor.sigMonitorValue.connect(self.wuserstatus.showMonitor)
        self.diffractometer.sigNoMonitorCounts.connect(self.wmain.changeLampColor)
        self.diffractometer.sigExperimentPaused.connect(self.pausedExperiment)

    def connectBlowerSignals(self):
        self.diffractometer.blower.sigTemperature.connect(self.wblower.updateTemperature)
        self.diffractometer.blower.sigTemperature.connect(self.scipts['blower']._setTemp)
        self.diffractometer.blower.sigConnected.connect(self.wblower.connectionSucceed)
        self.diffractometer.blower.sigError.connect(self.wblower.connectionFailed)
        self.wblower.sigConnect.connect(self.diffractometer.blower.connectToSpec)
        self.wblower.sigDisconnect.connect(self.diffractometer.blower.stop)
        self.wblower.sigRun.connect(self.diffractometer.blower.run)

    def connectCryoSignals(self):
        self.wcryo.sigRestart.connect(self.diffractometer.cryo.restart)
        self.wcryo.sigStop.connect(self.diffractometer.cryo.cstop)
        self.wcryo.sigPause.connect(self.diffractometer.cryo.pause)
        self.wcryo.sigResume.connect(self.diffractometer.cryo.resume)
        self.wcryo.sigTurboOn.connect(self.diffractometer.cryo.turboOn)
        self.wcryo.sigTurboOff.connect(self.diffractometer.cryo.turboOff)
        self.wcryo.sigCool.connect(self.diffractometer.cryo.cool)
        self.wcryo.sigRamp.connect(self.diffractometer.cryo.ramp)
        self.wcryo.sigPlat.connect(self.diffractometer.cryo.plat)
        self.wcryo.sigHold.connect(self.diffractometer.cryo.hold)
        self.wcryo.sigEnd.connect(self.diffractometer.cryo.end)
        self.wcryo.sigPurge.connect(self.diffractometer.cryo.purge)
        self.wcryo.sigConnect.connect(self.diffractometer.cryo.start)
        self.wcryo.sigDisconnect.connect(self.diffractometer.cryo.stop)
        self.diffractometer.cryo.sigError.connect(self.wcryo.cryoError)
        self.diffractometer.cryo.sigStatus.connect(self.wcryo.updateStatus)
        self.diffractometer.cryo.sigStatus.connect(self.scipts['cryostream']._setTemp)

    def connectScanSignals(self):
        self.diffractometer.scanman.sigPoint.connect(self.wscan.plotCurve)
        self.diffractometer.scanman.sigFit.connect(self.wscan.plotGauss)
        self.diffractometer.scanman.sigStopScan.connect(self.wscan.scanFinished)
        self.wscan.sigRun.connect(self.diffractometer.runScan)
        self.wscan.sigAbort.connect(self.diffractometer.abortScan)

    def connectLakeshoreSignals(self):
        self.wlakeshore.sigConnect.connect(self.diffractometer.lakeshore.start)
        self.wlakeshore.sigStop.connect(self.diffractometer.lakeshore.stop)
        self.wlakeshore.sigUpdateParameters.connect(self.diffractometer.lakeshore.updateParameters)
        self.wlakeshore.sigSetOutput.connect(self.diffractometer.lakeshore.setOutput)
        self.wlakeshore.sigSetParameters.connect(self.diffractometer.lakeshore.setParams)
        self.wlakeshore.sigSetSensor.connect(self.diffractometer.lakeshore.setSensor)
        self.diffractometer.lakeshore.sigError.connect(self.wlakeshore.lakeshoreError)
        self.diffractometer.lakeshore.sigParams.connect(self.wlakeshore.updateParams)
        self.diffractometer.lakeshore.sigStatus.connect(self.wlakeshore.updateTemp)

    def connectSequenceSignals(self):
        self.wmain.sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.wseq.sigStop.connect(self.diffractometer.abortExperiment)
        self.wseq.sigStop.connect(self.diffractometer.blower.pause)
        self.wseq.sigStop.connect(self.diffractometer.cryo.pause)
        self.wseq.sigStop.connect(self.wcryo.pause)
        self.wseq.sigStop.connect(self.wblower.pause)
        self.diffractometer.sigExperimentPaused.connect(self.wcryo.pause)
        self.diffractometer.sigExperimentResumed.connect(self.wcryo.resume)
        self.wblower.sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.wlakeshore.sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.wcryo.sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.wblower.sigCreateSeqAction.connect(lambda: self.wmain.actionSequence.setChecked(True))
        self.wcryo.sigCreateSeqAction.connect(lambda: self.wmain.actionSequence.setChecked(True))
        self.wlakeshore.sigCreateSeqAction.connect(lambda: self.wmain.actionSequence.setChecked(True))
        self.wmain.sigCreateSeqAction.connect(lambda: self.wmain.actionSequence.setChecked(True))
        self.wscripted.sigScript.connect(lambda: self.wmain.actionSequence.setChecked(True))
        self.wscripted.sigScript.connect(self.runScript)
        self.sigScriptError.connect(self.wscripted.qMsgError)
        self.scipts['diffractometer']._sigCreateSeqScanAction.connect(self.wmain.runFromScript)
        self.scipts['diffractometer']._sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.scipts['diffractometer']._sigSetScanTypeInGUI.connect(self.wmain.setScanType)
        self.scipts['blower']._sigCreateBlowerAction.connect(self.wblower.createAction)
        self.scipts['blower']._sigCreateBlowerWaitAction.connect(self.wseq.appendActionToSeqList)
        self.scipts['blower']._sigWaitFromSeq.connect(self.wblower.setSignalOnHold)
        self.scipts['cryostream']._sigHoldFromSeq.connect(self.wcryo.setSignalOnHold)
        self.scipts['cryostream']._sigCreateSeqAction.connect(self.wcryo.createAction)
        self.scipts['cryostream']._sigCreateSeqWaitAction.connect(self.wseq.appendActionToSeqList)
        self.scipts['lakeshore']._sigSet.connect(self.wlakeshore.setScriptParams)
        self.scipts['lakeshore']._sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)
        self.scipts['lakeshore']._sigHoldFromSeq.connect(self.wlakeshore.setSignalOnHold)
        self.scipts['motor']._sigDiffWait.connect(self.diffractometer.waitForMotorsMovementFromScript)
        self.scipts['motor']._sigMoveFromSeq.connect(self.diffractometer.moveMotor)
        self.scipts['motor']._sigMoveRelFromSeq.connect(self.diffractometer.moveMotorRelative)
        self.scipts['motor']._sigCreateSeqAction.connect(self.wseq.appendActionToSeqList)

    def createDiffractometer(self):
        self.diffractometer = diffractometer.Diffractometer()

    def start(self):
        self.loadSettings()
        self.woptions.loadSettings()

    def continueStart(self):
        if self.started:
            return
        self.started = True
        self.wmain.loadSettings()
        self.wuserstatus.loadSettings()
        self.wuserstatus.setupMotors()
        self.wstatus.loadSettings()
        self.wstatus.setupMotors()
        self.walign.loadSettings()
        self.walign.setupMotors()
        self.wrelmove.loadSettings()
        self.calcMax2Theta()
        self.calcDCTime()
        self.wmain.show()
        self.wlogging.show()
        self.wuserstatus.show()
        self.diffractometer.start()
        self.sigGUIStarted.emit()

    def loadSettings(self):
        s = self.settings
        motors = json.loads(s.value('Controller/Motors', '[]'))
        self.sigConnectMotors.emit(motors)
        self.motors = motors

    def saveSettings(self):
        s = self.settings
        s.setValue('Controller/Motors', json.dumps(self.motors))

    def stop(self):
        self.diffractometer.stop()
        self.saveSettings()
        self.wmain.close()
        self.wlogging.close()
        self.wstatus.close()
        self.wuserstatus.close()
        self.wrelmove.close()
        self.walign.close()
        self.wscan.close()
        self.wlakeshore.close()
        self.wblower.close()
        self.wcryo.close()
        self.wseq.close()
        self.wscripted.close()
        self.woptions.close()

    def showStatusWindow(self, checked):
        self.showWindowWithPassword(checked, self.wstatus, self.wmain.actionStatus)

    def showAlignWindow(self, checked):
        self.showWindowWithPassword(checked, self.walign, self.wmain.actionAlignment)

    def showWindowWithPassword(self, checked, window, action):
        checked = checked and GUtils.askPass(self.wmain)
        window.setVisible(checked)
        action.setChecked(checked)

    def addMotor(self, host, spec, motor):
        if host and spec and motor:
            motor = '{}->{}->{}'.format(host, spec, motor)
            if motor not in self.motors:
                self.motors.append(motor)
                self.sigConnectMotor.emit(motor)
                self.saveSettings()

    def removeMotor(self, motor):
        self.motors.remove(motor)
        self.saveSettings()

    def calcMax2Theta(self):
        if not self.wavelength:
            return
        pix = self.wmain.pixelxSpinBox.value()
        beamx = self.wmain.beamxSpinBox.value()
        R = (self.wmain.detectorxSpinBox.value() - (beamx - self.wmain.plvertSpinBox.value() / pix * 1e3)) * pix * 1e-3
        s = self.wmain.zeroSpinBox.value() + self.wmain.pldistdSpinBox.value() + self.wmain.pldistfSpinBox.value()
        if s == 0:
            return
        angle = math.atan(R / s)
        if angle == 0:
            return
        d = self.wavelength / 2. / math.sin(angle / 2.)
        self.sigMax2Theta.emit(math.degrees(angle), d)

    def calcDCTime(self):
        t = self.wmain.nframesSpinBox.value() * self.wmain.exposureSpinBox.value() * self.wmain.nperiodsSpinBox.value()
        totalMin = t / 60
        days, hours, minutes = utils.calcTime(totalMin)
        self.sigDCTime.emit(days, hours, minutes, totalMin)

    def setWavelength(self, wavelength, energy):
        self.wavelength = wavelength
        self.energy = energy
        self.calcMax2Theta()

    def setExperimentTime(self, opts=None):
        if opts:
            self.expTime = opts['nframes'] * opts['expPeriod'] * opts['periods']
        self.expStarted = time.time()
        self.expPaused = 0

    def calcExpTime(self):
        if self.expStarted:
            timeLeft = (self.expTime - time.time() + self.expStarted) / 60
            days, hours, minutes = utils.calcTime(timeLeft)
            msg = 'Time left'
        elif self.expPaused:
            timeStand = (time.time() - self.expPaused) / 60
            days, hours, minutes = utils.calcTime(timeStand)
            msg = 'Paused for'
        else:
            return
        if days and hours:
            t = f'{msg}: {days:d}d {hours:d}h {minutes:d}m'
        elif hours:
            t = f'{msg}: {hours:d}h {minutes:d}m'
        else:
            t = f'{msg}: {minutes:d}m'
        self.sigExpTimeLeft.emit(t)

    def pausedExperiment(self):
        self.expStarted = 0
        self.expPaused = time.time()

    def runScript(self, script):
        try:
            exec(script, self.scipts.copy())
        except SyntaxError as err:
            self.sigScriptError.emit(f'Python syntax error: {str(err)}')
        except Exception as err:
            self.sigScriptError.emit(str(err))
