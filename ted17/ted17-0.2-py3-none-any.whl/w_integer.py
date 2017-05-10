# -*- coding: utf-8 -*-
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
from .w_textline import Text_line


class Integer(Text_line):
    '''
    Text field with numeric chars only left aligned.
    '''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)

        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)
