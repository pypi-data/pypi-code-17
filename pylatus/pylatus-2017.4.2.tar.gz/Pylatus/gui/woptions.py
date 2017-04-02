#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from .ui.ui_options import Ui_Ui_Settings


class WOptions(QtWidgets.QDialog, Ui_Ui_Settings):
    sigConfig = QtCore.pyqtSignal(object)

    def __init__(self, parent, settings):
        super().__init__(parent=parent)
        self.settings = settings
        self.config = None
        self.setUI()

    def setUI(self):
        self.setupUi(self)
        self.editReadout1.setValidator(QtGui.QDoubleValidator())
        self.editReadout2.setValidator(QtGui.QDoubleValidator())
        self.editSeparator.setValidator(QtGui.QIntValidator())
        self.editNoBeamCounts.setValidator(QtGui.QIntValidator())
        self.editMusstTimeout1.setValidator(QtGui.QDoubleValidator())
        self.editMusstTimeout2.setValidator(QtGui.QDoubleValidator())
        self.editNumberOfFilters.setValidator(QtGui.QIntValidator())
        self.editBeamstopOn.setValidator(QtGui.QDoubleValidator())
        self.editBeamstopOff.setValidator(QtGui.QDoubleValidator())
        self.editScanTime.setValidator(QtGui.QDoubleValidator())
        self.editScanRange.setValidator(QtGui.QDoubleValidator())
        self.editScanStep.setValidator(QtGui.QDoubleValidator())
        self.editScanFilter.setValidator(QtGui.QIntValidator())

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WOptions/Geometry', QtCore.QByteArray()))
        self.editDetAddress.setText(s.value('WOptions/DetAddress', '10.10.10.100:41234'))
        self.editReadout1.setText(s.value('WOptions/Readout1', '0.0023'))
        self.editReadout2.setText(s.value('WOptions/Readout2', '0.0130'))
        self.editSeparator.setText(s.value('WOptions/Separator', '24'))
        self.editServerDir.setText(s.value('WOptions/ServerDir', '/ramdisk/'))
        self.editLogFile.setText(s.value('WOptions/LogFile', 'pylatus.log'))
        self.editUserDir.setText(s.value('WOptions/UserDir', '/data/users/'))
        self.editDataDir.setText(s.value('WOptions/DataDir', '/ramdisk/500_500'))
        self.editNoBeamCounts.setText(s.value('WOptions/NoBeamCounts', '10'))
        self.editMonitorSpec.setText(s.value('WOptions/MonitorSpec', 'snbla1.esrf.fr:monitor:mon'))
        self.editMusstSpec.setText(s.value('WOptions/MusstSpec', 'snbla1.esrf.fr:rhmusst'))
        self.editMusstTimeout1.setText(s.value('WOptions/MusstTimeout1', '0'))
        self.editMusstTimeout2.setText(s.value('WOptions/MusstTimeout2', '0'))
        self.editMusstFirmware.setText(s.value('WOptions/mfw', '/users/blissadm/local/isg/musst/pilatus_bm01.mprg'))
        self.editNumberOfFilters.setText(s.value('WOptions/NumberOfFilters', '10'))
        self.editBeamstopOn.setText(s.value('WOptions/BeamstopOn', '0'))
        self.editBeamstopOff.setText(s.value('WOptions/BeamstopOff', '6'))
        self.editRootHash.setText(s.value('WOptions/roothash', 'e55761e10506cc773791f579b058c9d845e2a14a'))
        self.editMono.setText(s.value('WOptions/mono', 'mono'))
        self.editPhi.setText(s.value('WOptions/phi', 'phi'))
        self.editPrphi.setText(s.value('WOptions/prphi', 'prphi'))
        self.editOmega.setText(s.value('WOptions/omega', 'omega'))
        self.editKappa.setText(s.value('WOptions/kappa', 'kappa'))
        self.editBstop.setText(s.value('WOptions/bstop', 'bstop'))
        self.editPldistf.setText(s.value('WOptions/pldistf', 'pldistf'))
        self.editPldistd.setText(s.value('WOptions/pldistd', 'pldistd'))
        self.editPlvert.setText(s.value('WOptions/plvert', 'plvert'))
        self.editPlrot.setText(s.value('WOptions/plrot', 'plrot'))
        self.editPrver.setText(s.value('WOptions/prver', 'prver'))
        self.editPrhor.setText(s.value('WOptions/prhor', 'prhor'))
        self.editFilter.setText(s.value('WOptions/filter', 'filter'))
        self.editScanAxis.setText(s.value('WOptions/ScanAxis', 'mirror4'))
        self.editScanTime.setText(s.value('WOptions/ScanTime', '0.1'))
        self.editScanRange.setText(s.value('WOptions/ScanRange', '0.012'))
        self.editScanStep.setText(s.value('WOptions/ScanStep', '0.001'))
        self.editScanFilter.setText(s.value('WOptions/ScanFilter', '7'))
        self.on_applyButton_clicked()

    def saveSettings(self):
        s = self.settings
        s.setValue('WOptions/Geometry', self.saveGeometry())
        s.setValue('WOptions/DetAddress', self.editDetAddress.text())
        s.setValue('WOptions/Readout1', self.editReadout1.text())
        s.setValue('WOptions/Readout2', self.editReadout2.text())
        s.setValue('WOptions/Separator', self.editSeparator.text())
        s.setValue('WOptions/ServerDir', self.editServerDir.text())
        s.setValue('WOptions/LogFile', self.editLogFile.text())
        s.setValue('WOptions/UserDir', self.editUserDir.text())
        s.setValue('WOptions/DataDir', self.editDataDir.text())
        s.setValue('WOptions/NoBeamCounts', self.editNoBeamCounts.text())
        s.setValue('WOptions/MonitorSpec', self.editMonitorSpec.text())
        s.setValue('WOptions/MusstSpec', self.editMusstSpec.text())
        s.setValue('WOptions/MusstTimeout1', self.editMusstTimeout1.text())
        s.setValue('WOptions/MusstTimeout2', self.editMusstTimeout2.text())
        s.setValue('WOptions/mfw', self.editMusstFirmware.text())
        s.setValue('WOptions/NumberOfFilters', self.editNumberOfFilters.text())
        s.setValue('WOptions/BeamstopOn', self.editBeamstopOn.text())
        s.setValue('WOptions/BeamstopOff', self.editBeamstopOff.text())
        s.setValue('WOptions/roothash', self.editRootHash.text())
        s.setValue('WOptions/mono', self.editMono.text())
        s.setValue('WOptions/phi', self.editPhi.text())
        s.setValue('WOptions/prphi', self.editPrphi.text())
        s.setValue('WOptions/omega', self.editOmega.text())
        s.setValue('WOptions/kappa', self.editKappa.text())
        s.setValue('WOptions/bstop', self.editBstop.text())
        s.setValue('WOptions/pldistf', self.editPldistf.text())
        s.setValue('WOptions/pldistd', self.editPldistd.text())
        s.setValue('WOptions/plvert', self.editPlvert.text())
        s.setValue('WOptions/plrot', self.editPlrot.text())
        s.setValue('WOptions/prver', self.editPrver.text())
        s.setValue('WOptions/prhor', self.editPrhor.text())
        s.setValue('WOptions/filter', self.editFilter.text())
        s.setValue('WOptions/ScanAxis', self.editScanAxis.text())
        s.setValue('WOptions/ScanTime', self.editScanTime.text())
        s.setValue('WOptions/ScanRange', self.editScanRange.text())
        s.setValue('WOptions/ScanStep', self.editScanStep.text())
        s.setValue('WOptions/ScanFilter', self.editScanFilter.text())

    @QtCore.pyqtSlot()
    def on_applyButton_clicked(self):
        config = self.optionsToConfig()
        self.config = config
        self.sigConfig.emit(config)
        self.close()

    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()

    def optionsToConfig(self):
        class Config:
            pass

        c = Config()
        for objName in self.__dict__:
            obj = self.__dict__[objName]
            if isinstance(obj, QtWidgets.QLineEdit):
                name = objName[4].lower() + objName[5:]
                setattr(c, name, obj.text())
        return c

    def configToOptions(self):
        if self.config:
            for name in self.config.__dict__:
                objName = 'edit' + name[0].upper() + name[1:]
                obj = getattr(self, objName)
                if isinstance(obj, QtWidgets.QLineEdit):
                    obj.setText(self.config.__dict__[name])

    def showEvent(self, event):
        self.optionsToConfig()
        super().showEvent(event)

    def closeEvent(self, event):
        self.configToOptions()
        super().closeEvent(event)
        self.hide()
        self.saveSettings()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
