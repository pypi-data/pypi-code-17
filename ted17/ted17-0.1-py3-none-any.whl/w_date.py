# -*- coding: utf-8 -*-

import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
from . import parameters as par


class Date(Qw.QDateEdit):

    '''
    Date values for most cases
    '''

    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setCalendarPopup(True)
        self.setDisplayFormat(par.GREEK_DATE_FORMAT)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setMaximumWidth(par.DATE_MAX_WIDTH)
        # self.setMinimumWidth(par.DATE_MAX_WIDTH)
        self.setMaximumHeight(par.MAX_HEIGHT)
        self.setLocale(par.grlocale)

    def set(self, sqliteDate):
        if sqliteDate:
            if len(sqliteDate) > 10:
                sqliteDate = sqliteDate[:10]
            yr, mn, dt = sqliteDate.split('-')
            qd = Qc.QDate()
            qd.setDate(int(yr), int(mn), int(dt))
            self.setDate(qd)
        else:
            self.setDate(Qc.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(par.SQLITE_DATE_FORMAT)
