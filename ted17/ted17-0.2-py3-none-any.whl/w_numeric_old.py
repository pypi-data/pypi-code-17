# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
from . import parameters as par
from . import dec


class Numeric(Qw.QLineEdit):

    '''
    Text field with numeric chars only.
    '''

    def __init__(self, val='0', parent=None):
        super().__init__(parent)
        self.set(val)
        rval = Qc.QRegExp('(\d*)([1-9,])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)

    # def keyPressEvent(self, ev):
    #     # Check if keypressed is '.'
    #     if ev.key() == 46:
    #         if ',' in self.text():
    #             pass
    #         else:
    #             self.setText(self.text() + ',')
    #     elif ev.key() in (Qc.Qt.Key_Return, Qc.Qt.Key_Enter):
    #         self.set(self.get())
    #     Qw.QLineEdit.keyPressEvent(self, ev)

    def focusOutEvent(self, ev):
        self.set(self.get())
        Qw.QLineEdit.focusOutEvent(self, ev)

    # def focusInEvent(self, ev):
    #     self.selectAll()
    #     Qw.QLineEdit.focusInEvent(self, ev)

    def set(self, txt):
        if txt:
            self.setText(dec.dec2gr(txt))
        else:
            self.setText(dec.dec2gr(0))

    def get(self):
        greek_div = ','
        normal_div = '.'
        tmp = '%s' % self.text()
        tmp = tmp.replace(normal_div, '')
        tmp = tmp.replace(greek_div, normal_div)
        return dec.dec(tmp.strip())
