# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
from . import parameters as par


class Checkbox(Qw.QCheckBox):

    """
    True or False field
    Gets / Sets two values : 0 for unchecked , 2 for checked
    """

    def __init__(self, val=False, parent=None):
        super().__init__(parent)

        self.set(val)

        self.setMinimumHeight(par.MIN_HEIGHT)

    def set(self, txtVal):
        if txtVal:
            self.setChecked(txtVal)
        else:
            self.setChecked(False)

    def get(self):
        return self.checkState() != 0
