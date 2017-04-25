# -*- coding: utf-8 -*-

#    `ionics` is a software which models various ionization cross sections.
#    Copyright (C) 2017  Dominik Vilsmeier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

import ionics
import inspect
import os

from PyQt4 import QtGui, QtCore


class InteractiveFileBrowser(QtGui.QTreeView):
    clear_cross_sections = QtCore.pyqtSignal()
    file_selected = QtCore.pyqtSignal('QString')
    dir_selected = QtCore.pyqtSignal('QString')

    def __init__(self, parent=None):
        super(InteractiveFileBrowser, self).__init__(parent)

        root_dir = os.path.dirname(inspect.getfile(ionics))

        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(root_dir)
        self.model.setNameFilters(['*.py'])
        self.model.setNameFilterDisables(False)
        self.setModel(self.model)

        self.setRootIndex(self.model.index(root_dir))

        self.clicked.connect(self.custom_clicked)

    def custom_clicked(self, index):
        if self.model.isDir(index):
            self.clear_cross_sections.emit()
            it = QtCore.QDirIterator(self.model.filePath(index), QtCore.QStringList() << "*.py")
            fp = it.next()
            while fp:
                self.dir_selected.emit(fp)
                fp = it.next()
        else:
            self.file_selected.emit(self.model.filePath(index))
