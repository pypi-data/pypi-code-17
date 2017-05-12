#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pyqtgraph as pg
import cryio
from .ui.wmask import Ui_WMask


class WMask(QtWidgets.QDialog, Ui_WMask):
    def __init__(self, edit, itype, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.loadSettings()
        self.lessEdit.setValidator(QtGui.QIntValidator())
        self.moreEdit.setValidator(QtGui.QIntValidator())
        self.edit = edit
        self.itype = itype
        self.beamline = ''
        self.roi = []
        self.data = None

    def saveSettings(self):
        s = QtCore.QSettings()
        s.setValue('WMask/Geometry', self.saveGeometry())
        s.setValue('WMask/less', self.lessEdit.text())
        s.setValue('WMask/more', self.moreEdit.text())
        s.setValue('WMask/folder', self.folder)

    def loadSettings(self):
        s = QtCore.QSettings()
        self.restoreGeometry(s.value('WMask/Geometry', QtCore.QByteArray()))
        self.lessEdit.setText(s.value('WMask/less', '0'))
        self.moreEdit.setText(s.value('WMask/more', '0'))
        self.folder = s.value('WMask/folder', '')

    def closeEvent(self, event):
        self.saveSettings()

    def changeBeamline(self, beamline):
        self.beamline = beamline

    @QtCore.pyqtSlot()
    def on_openImageButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        image = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image file', self.folder, 'Frames (*.edf *.cbf)')[0]
        if image:
            self.folder = os.path.dirname(image)
            data = cryio.openImage(image).array
            if self.beamline == 'SNBL':
                data = np.rot90(data[::-1], 3)
            elif self.beamline == 'Dubble':
                if self.itype == 'saxs':
                    data = np.rot90(data, 3)
                elif self.itype == 'waxs':
                    data = np.rot90(data, 1)
            self.data = data
            self.imageView.setImage(data)
            self.setWindowTitle('Mask - {}'.format(image))

    def getImageCenter(self):
        ranges = self.imageView.getView().getState()['viewRange']
        return ranges[0][1] // 2, ranges[1][1] // 2

    @QtCore.pyqtSlot()
    def on_polyButton_clicked(self):
        xc, yc = self.getImageCenter()
        self.addRoi(PolyLineROI([[xc, yc], [xc-100, yc-100], [xc-100, yc+100]], closed=True, removable=True))

    @QtCore.pyqtSlot()
    def on_ellipseButton_clicked(self):
        xc, yc = self.getImageCenter()
        self.addRoi(EllipseROI([xc, yc], [100, 100], removable=True))

    def addRoi(self, roi):
        self.roi.append(roi)
        self.imageView.getView().addItem(roi)
        roi.sigRemoveRequested.connect(self.removeRoi)

    def removeRoi(self, roi):
        self.imageView.getView().removeItem(roi)
        self.roi.remove(roi)

    def makeMask(self):
        image = self.imageView.getImageItem()
        mask = np.zeros(self.data.shape, dtype=np.int8)
        for roi in self.roi:
            array, coords = roi.getArrayRegion(self.data, image)
            if array is None:
                continue
            array[array != 0] = 1
            coords[coords < 0] = 0
            xcoords, ycoords = coords.round().astype(np.int32)
            xcoords[xcoords > mask.shape[0] - 1] = mask.shape[0] - 1
            ycoords[ycoords > mask.shape[1] - 1] = mask.shape[1] - 1
            mask[xcoords, ycoords] = array
        less, more = self.getLessMore()
        if less is not None:
            mask[self.data <= less] = 1
        if more is not None:
            mask[self.data >= more] = 1
        return mask

    def getLessMore(self):
        less, more = None, None
        if self.lessCheckbox.isChecked():
            less = int(self.lessEdit.text())
        if self.moreCheckbox.isChecked():
            more = int(self.moreEdit.text())
        return less, more

    def saveApplyMask(self, name, mask):
        np.savez_compressed(name, mask)
        self.edit.setText(name)

    @QtCore.pyqtSlot()
    def on_applyButton_clicked(self):
        if self.data is not None:
            mask = self.makeMask()
            name = tempfile.mkstemp(suffix='.npz')[1]
            self.saveApplyMask(name, mask)
            self.close()

    @QtCore.pyqtSlot()
    def on_clearButton_clicked(self):
        for roi in self.roi:
            self.imageView.getView().removeItem(roi)
        self.imageView.clear()
        self.setWindowTitle('Mask')
        self.data = None
        self.roi = []

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_saveMaskButton_clicked(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save mask', self.folder, 'Bubble mask (*.npz)')[0]
        if name:
            if not name.endswith('.npz'):
                name = '{}.npz'.format(name)
            mask = self.makeMask()
            self.saveApplyMask(name, mask)

    @QtCore.pyqtSlot()
    def on_saveROIButton_clicked(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save mask ROI', self.folder, 'Bubble mask ROI (*.roi)')[0]
        if name:
            if not name.endswith('.roi'):
                name = '{}.roi'.format(name)
            less, more = self.getLessMore()
            roi = []
            for r in self.roi:
                state = r.saveState()
                if isinstance(r, PolyLineROI):
                    state['type'] = 'PolyLineROI'
                elif isinstance(r, EllipseROI):
                    state['type'] = 'EllipseROI'
                roi.append(state)
            json.dump({'roi': roi, 'less': less, 'more': more}, open(name, 'w'))

    @QtCore.pyqtSlot()
    def on_loadROIButton_clicked(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load mask ROI', self.folder, 'Bubble mask ROI (*.roi)')[0]
        if name:
            froi = json.load(open(name, 'r'))
            self.lessEdit.setText(froi['less'])
            self.moreEdit.setText(froi['more'])
            for state in froi['roi']:
                if state['type'] == 'PolyLineROI':
                    roi = PolyLineROI([[1, 1], [0, 0], [0, 2]], closed=True, removable=True)
                elif state['type'] == 'EllipseROI':
                    roi = EllipseROI([0, 0], [1, 1], removable=True)
                else:
                    continue
                self.addRoi(roi)
                roi.setState(state)


class PolyLineROI(pg.PolyLineROI):
    def getArrayRegion(self, data, img, axes=(0, 1), **kwds):
        s, m = pg.ROI.getArrayRegion(self, data, img, axes=axes, fromBoundingRect=True, returnMappedCoords=True, **kwds)
        if s is None:
            return None, None
        if img.axisOrder == 'col-major':
            mask = self.renderShapeMask(s.shape[axes[0]], s.shape[axes[1]])
        else:
            mask = self.renderShapeMask(s.shape[axes[1]], s.shape[axes[0]])
            mask = mask.T
        shape = [1] * data.ndim
        shape[axes[0]] = s.shape[axes[0]]
        shape[axes[1]] = s.shape[axes[1]]
        mask = mask.reshape(shape)
        return s * mask, m


class EllipseROI(pg.EllipseROI):
    def getArrayRegion(self, arr, img=None, axes=(0, 1), **kwds):
        arr, m = pg.ROI.getArrayRegion(self, arr, img, axes, returnMappedCoords=True, **kwds)
        if arr is None or arr.shape[axes[0]] == 0 or arr.shape[axes[1]] == 0:
            return None, None
        w = arr.shape[axes[0]]
        h = arr.shape[axes[1]]
        mask = np.fromfunction(lambda x, y: (((x+0.5)/(w/2)-1)**2 + ((y+0.5)/(h/2)-1)**2)**0.5 < 1, (w, h))
        if axes[0] > axes[1]:
            mask = mask.T
        shape = [(n if i in axes else 1) for i, n in enumerate(arr.shape)]
        mask = mask.reshape(shape)
        return arr * mask, m
