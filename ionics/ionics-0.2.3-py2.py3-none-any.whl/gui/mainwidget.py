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

from . import pyqt45
from .cross_section_view import CrossSectionView
from .fileview import InteractiveFileBrowser
from .plotcontainer import PlotContainer

QtCore = pyqt45.QtCore
Widgets = pyqt45.Widgets


class MainWidget(Widgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.cross_section_view = CrossSectionView(self)
        self.file_view = InteractiveFileBrowser(self)
        self.plot_view = PlotContainer(self.cross_section_view)
        scroll_area = Widgets.QScrollArea()
        scroll_area.setWidget(self.plot_view)
        scroll_area.setWidgetResizable(True)

        v_splitter = Widgets.QSplitter()
        v_splitter.setOrientation(QtCore.Qt.Vertical)
        v_splitter.addWidget(self.file_view)
        v_splitter.addWidget(self.cross_section_view)

        h_splitter = Widgets.QSplitter()
        h_splitter.setOrientation(QtCore.Qt.Horizontal)
        h_splitter.addWidget(v_splitter)
        h_splitter.addWidget(scroll_area)

        h_layout = Widgets.QHBoxLayout()
        h_layout.addWidget(h_splitter)

        self.setLayout(h_layout)

        self.file_view.clear_cross_sections.connect(self.cross_section_view.clear_cross_sections)
        self.file_view.file_selected.connect(self.cross_section_view.file_selected)
        self.file_view.dir_selected.connect(self.cross_section_view.dir_selected)
