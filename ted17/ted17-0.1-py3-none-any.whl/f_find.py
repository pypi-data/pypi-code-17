# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from tedutil import dec
from tedutil import db
from decimal import Decimal as tdec


class sortWidgetItem(Qw.QTableWidgetItem):
    """
    """
    def __init__(self, text, sortKey):
        super().__init__(text, Qw.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


def item_int(num):
    item = Qw.QTableWidgetItem()
    # item.setData(QtCore.Qt.DisplayRole, QtCore.QVariant(num))
    item.setData(Qc.Qt.DisplayRole, num)
    item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    return item


def item_num(num):
    item = sortWidgetItem(dec.dec2gr(num), num)
    item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    return item


def item_str(strv):
    st = '%s' % strv
    if st == 'None':
        st = ''
    item = Qw.QTableWidgetItem(st)
    return item


def item_date(strv):
    strv = '%s' % strv
    if len(strv) < 10:
        item = sortWidgetItem(strv, strv)
    else:
        y, m, d = strv.split('-')
        item = sortWidgetItem('%s/%s/%s' % (d, m, y), strv)
    return item


class Find(Qw.QDialog):
    signal_selected_id = Qc.pyqtSignal(str)
    signal_make_new = Qc.pyqtSignal(str)

    def __init__(self, dbf, sql, lbl, parent=None, frm=None,
                 sclose=True, title=None):
        """
        dbf : Database file path
        sql : final sql to run
        lbl : column labels
        frm : Name of the form to edit or add records
        sclose : True if immediately closing form after record selection
                 False otherwise
        title : Form Title
        """
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(title)
        # Save initialization data
        self.dbf = dbf
        self.sql = sql
        self.lbl = lbl
        self.parent = parent
        self.frm = frm
        self.sclose = sclose
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        self.tbl = Qw.QTableWidget()
        self.tbl.cellDoubleClicked.connect(self.get_values)
        self.tbl.verticalHeader().setStretchLastSection(False)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.tbl.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        self.tbl. setAlternatingRowColors(True)
        # self.setStyleSheet("alternate-background-color: rgba(208,246,230);")
        self.tbl.setSortingEnabled(True)
        self.tbl.wordWrap()
        layout.addWidget(self.tbl)
        self.resize(900, 700)
        self.populate()

    def contextMenuEvent(self, event):
        menu = Qw.QMenu(self)
        Action = menu.addAction(u"Δημιουργία νέας παρόμοιας εγγραφής")
        Action.triggered.connect(self.make_new)
        menu.exec_(event.globalPos())

    def make_new(self):
        i = self.tbl.currentRow()
        self.signal_make_new.emit('%s' % self.tbl.item(i, 0).text())

    def populate(self):
        rows = db.rowst(self.dbf, self.sql)
        self.tbl.setRowCount(len(rows))
        self.tbl.setColumnCount(len(self.lbl))
        self.tbl.setHorizontalHeaderLabels(self.lbl)
        total = dec.dec(0)
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                if dec.isNum(col):
                    if self.lbl[j][-2:] == 'id':
                        self.tbl.setItem(i, j, item_int(col))
                    elif type(col) is tdec:
                        self.tbl.setItem(i, j, item_num(col))
                    else:
                        # self.setItem(i, j, self._numItem(col))
                        self.tbl.setItem(i, j, item_num(col))
                elif (len(col) == 10) and (col[4] == '-'):
                    self.tbl.setItem(i, j, item_date(col))
                else:
                    self.tbl.setItem(i, j, item_str(col))
            total += dec.dec(row[-2]) - dec.dec(row[-1])
            self.tbl.setItem(i, len(self.lbl) - 1, item_num(total))
        self.tbl.resizeColumnsToContents()

    def get_values(self):
        i = self.tbl.currentRow()
        self.signal_selected_id.emit('%s' % self.tbl.item(i, 0).text())
        if self.sclose:
            self.accept()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == Qc.Qt.Key_Enter or
                ev.key() == Qc.Qt.Key_Return):
            self.get_values()
        Qw.QDialog.keyPressEvent(self, ev)

    @Qc.pyqtSlot()
    def slot_updated(self):
        self.populate()
