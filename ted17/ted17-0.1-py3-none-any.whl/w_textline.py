# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
from . import parameters as par


class Text_line(Qw.QLineEdit):

    """Text Line Class"""

    def __init__(self, val='', parent=None):
        super().__init__(parent)

        self.set(val)

        self.setMinimumHeight(par.MIN_HEIGHT)

    def set(self, txt):
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')
        self.setCursorPosition(0)

    def get(self):
        tmp = '%s' % self.text()
        return tmp.strip()
