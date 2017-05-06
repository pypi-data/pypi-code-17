# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from . import dec
from decimal import Decimal as tdec


class sortWidgetItem(Qw.QTableWidgetItem):
    """
    """
    def __init__(self, text, sortKey):
        super().__init__(text, Qw.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


class Table_widget(Qw.QTableWidget):
    """
    """
    def __init__(self, labels=[], rows=[[]], parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.rows = rows
        self.labels = labels
        self.parent = parent
        # Εδώ ορίζουμε το πλάτος της γραμμής του grid
        # self.verticalHeader().setDefaultSectionSize(20)
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        # self.setStyleSheet("alternate-background-color: rgba(208,246,230);")
        self.setSortingEnabled(True)
        self.populate()
        self.wordWrap()

    def _intItem(self, num):
        item = Qw.QTableWidgetItem()
        # item.setData(QtCore.Qt.DisplayRole, QtCore.QVariant(num))
        item.setData(Qc.Qt.DisplayRole, num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _numItem(self, num):
        item = sortWidgetItem(dec.dec2gr(num), num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _strItem(self, strv):
        st = '%s' % strv
        if st == 'None':
            st = ''
        item = Qw.QTableWidgetItem(st)
        return item

    def _dateItem(self, strv):
        strv = '%s' % strv
        if len(strv) < 10:
            item = sortWidgetItem(strv, strv)
        else:
            y, m, d = strv.split('-')
            item = sortWidgetItem('%s/%s/%s' % (d, m, y), strv)
        return item

    def populate(self):
        self.setRowCount(len(self.rows))
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)

        for i, row in enumerate(self.rows):
            for j, col in enumerate(row):
                if dec.isNum(col):
                    if self.labels[j][-2:] == 'id':
                        self.setItem(i, j, self._intItem(col))
                    elif type(col) is tdec:
                        self.setItem(i, j, self._numItem(col))
                    else:
                        # self.setItem(i, j, self._numItem(col))
                        self.setItem(i, j, self._strItem(col))
                elif (len(col) == 10) and (col[4] == '-'):
                    self.setItem(i, j, self._dateItem(col))
                else:
                    self.setItem(i, j, self._strItem(col))
        self.resizeColumnsToContents()


class Form_find(Qw.QDialog):
    valselected = Qc.pyqtSignal(str)

    def __init__(self, lbls, rws, title, parent=None, selectAndClose=True):
        super().__init__(parent)
        self.selectAndClose = selectAndClose
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        layout = Qw.QVBoxLayout()
        self.tbl = Table_widget(lbls, rws, parent)
        self.tbl.cellDoubleClicked.connect(self._setvals)
        layout.addWidget(self.tbl)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.resize(900, 700)

    def _setvals(self):
        self.vals = []
        i = self.tbl.currentRow()
        for j in range(self.tbl.columnCount()):
            self.vals.append(self.tbl.item(i, j).text())
        self.valselected.emit('%s' % self.vals[0])
        if self.selectAndClose:
            self.accept()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == Qc.Qt.Key_Enter or
                ev.key() == Qc.Qt.Key_Return):
            self._setvals()
        Qw.QDialog.keyPressEvent(self, ev)
