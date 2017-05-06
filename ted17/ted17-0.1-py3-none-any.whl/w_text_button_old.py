# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .f_table import Form_find
from .db import dataFromDB
from .grup import grup


class Text_button(Qw.QLineEdit):
    """Button text class """
    # SIGNALS HERE
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, val, qu1, qu9, db, parent=None):
        '''
        val : The actual value
        qu1 : SQL for getting the rpr of the val
        qu9 : SQL for getting pair of (val, rpr)
        db  : Database to use for the querying
        '''
        super().__init__(parent)
        self.button = Qw.QToolButton(self)
        self.red()  # We start with red Button
        self.textChanged.connect(self.edChanged)
        self.button.setCursor(Qc.Qt.ArrowCursor)
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        self.button.clicked.connect(self.buttonClicked)
        f_width = self.style().pixelMetric(Qw.QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()
        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' %
                           (button_size.width() + f_width + 1))
        self.qu1 = qu1
        self.qu9 = qu9
        self.db = db
        self.set(val)
        self.setToolTip(self.vap)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        f_width = self.style().pixelMetric(Qw.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - f_width - button_size.width(),
            (self.rect().bottom() - button_size.height() + 1) / 2)
        self.setCursorPosition(0)
        super(Text_button, self).resizeEvent(event)

    def _set(self, val, vap, isGreen):
        self.val = val
        self.vap = vap
        self.setText(vap)
        if isGreen:
            self.green()
        else:
            self.red()

    def set(self, val):
        if not val:
            self._set('', '', False)
        else:
            vfromdb = dataFromDB(self.db, self.qu1 % val)
            if len(vfromdb) == 1:
                self._set(val, vfromdb[0][0], True)
            else:
                # There is not an rpr from database
                self._set('', '', False)

    def get(self):
        if self.isGreen:
            return '%s' % self.val
        else:
            return ''

    def edChanged(self):
        if self.vap != self.text():
            self.red()
        else:
            self.green()

    def buttonClicked(self):
        self.button.setFocus()
        self.find('')

    def green(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(0, 180, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('...')
        self.isGreen = True

    def red(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(220, 50, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('...')
        self.isGreen = False

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.vap != self.text():
                self.find(self.text())
        return Qw.QLineEdit.keyPressEvent(self, ev)

    def find(self, text):
        oldvalue = self.get()
        sql = self.qu9 % grup(text)  # Convert it to python text
        vals = dataFromDB(self.db, sql)
        if len(vals) == 1:
            self._set(vals[0][0], vals[0][1], True)
        elif len(vals) > 1:
            tf = Form_find([u'κωδ', u'Περιγραφή'], vals, u'Αναζήτηση', self)
            if tf.exec_() == Qw.QDialog.Accepted:
                assert len(tf.vals) == 2
                self._set(tf.vals[0], tf.vals[1], True)
            else:
                if oldvalue == self.get():
                    pass
                else:
                    self.red()
        else:
            self.valNotFound.emit(self.text())
        self.setCursorPosition(0)
        self.setToolTip(self.vap)
