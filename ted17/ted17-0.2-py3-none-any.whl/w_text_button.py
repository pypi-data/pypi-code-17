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


class Text_button(Qw.QWidget):
    """Button text class """
    # SIGNALS HERE
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, val, qu1, qu9, dbf, parent=None):
        '''
        val : The actual value
        qu1 : SQL for getting the rpr of the val
        qu9 : SQL for getting pair of (val, rpr)
        dbf : Database file to use for the querying
        '''
        super().__init__(parent)
        self.text = Qw.QLineEdit(self)
        self.button = Qw.QToolButton(self)
        layout = Qw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.red()  # We start with red Button
        self.text.textChanged.connect(self.text_changed)
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        self.button.clicked.connect(self.button_clicked)
        self.qu1 = qu1
        self.qu9 = qu9
        self.dbf = dbf
        self.set(val)

    def _set(self, val, vap, isGreen):
        self.val = val
        self.vap = vap
        self.text.setText(vap)
        self.setToolTip(self.vap)
        self.text.setCursorPosition(0)
        if isGreen:
            self.green()
        else:
            self.red()

    def set(self, val):
        if not val:
            self._set('', '', False)
        else:
            vfromdb = dataFromDB(self.dbf, self.qu1 % val)
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

    def text_changed(self):
        if self.vap != self.text.text():
            self.red()
        else:
            self.green()

    def button_clicked(self):
        self.button.setFocus()
        self.find('')

    def green(self):
        # self.button.setStyleSheet(
        #     'border: 0px; padding: 0px; background-color: rgba(0, 180, 0); '
        #     'color: rgb(255, 255, 255);')
        self.button.setStyleSheet('background-color: rgba(0, 180, 0);')
        self.button.setText('?')
        self.isGreen = True

    def red(self):
        self.button.setStyleSheet('background-color: rgba(239, 41, 41);')
        # self.button.setStyleSheet(
        #     'border: 0px; padding: 0px; background-color: rgba(220, 50, 0); '
        #     'color: rgb(255, 255, 255);')
        self.button.setText('?')
        self.isGreen = False

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.vap != self.text.text():
                self.find(self.text.text())
        return Qw.QWidget.keyPressEvent(self, ev)

    def find(self, text):
        oldvalue = self.get()
        sql = self.qu9 % grup(text)  # Convert it to python text
        vals = dataFromDB(self.dbf, sql)
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
            self.valNotFound.emit(self.text.text())
        # self.text.setCursorPosition(0)
        self.setToolTip(self.vap)
