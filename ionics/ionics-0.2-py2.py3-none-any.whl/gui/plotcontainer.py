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

from PyQt4 import QtGui, QtCore

from .plotview import PlotView


class PlotContainer(QtGui.QWidget):
    def __init__(self, cross_section_view, parent=None):
        super(PlotContainer, self).__init__(parent)

        self.cross_section_view = cross_section_view

        self.plots = [PlotView(self.cross_section_view, self)]
        self.add_button = QtGui.QPushButton('add')
        self.add_button.setFixedSize(QtCore.QSize(40, 30))
        self.add_button.clicked.connect(self.add_plot)

        self.splitter = QtGui.QSplitter()
        self.splitter.addWidget(self.plots[0])

        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(self.splitter, 1)
        h_layout.addWidget(self.add_button, 0)
        self.setLayout(h_layout)

    def add_plot(self):
        self.plots.append(PlotView(self.cross_section_view, self))
        self.splitter.insertWidget(self.splitter.count(), self.plots[-1])
