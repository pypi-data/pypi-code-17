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

    def set(self, iso_date):
        if iso_date:
            if len(iso_date) > 10:
                iso_date = iso_date[:10]
            yyy, mmm, ddd = iso_date.split('-')
            qdate = Qc.QDate()
            qdate.setDate(int(yyy), int(mmm), int(ddd))
            self.setDate(qdate)
        else:
            self.setDate(Qc.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(par.SQLITE_DATE_FORMAT)
