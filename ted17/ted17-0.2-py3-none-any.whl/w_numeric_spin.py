# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from . import parameters as par
from . import dec


class Numeric_spin(Qw.QDoubleSpinBox):

    '''
    Numeric (decimal 2 ) values (eg 999,99)
    '''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)

        self.set(val)

        self.setMinimum(-99999999999)
        self.setMaximum(99999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setSingleStep(0)  # Για να μην αλλάζει η τιμή με τα βελάκια
        self.setGroupSeparatorShown(True)
        self.setLocale(par.grlocale)

    def get(self):
        return dec.dec(self.value())

    def set(self, val):
        if val:
            self.setValue(val)
        else:
            self.setValue(0)
