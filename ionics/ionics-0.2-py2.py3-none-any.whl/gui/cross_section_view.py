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

import inspect

from PyQt4 import QtGui


class CrossSectionContainer(QtGui.QListWidgetItem):
    def __init__(self, title, cross_section, parent=None):
        super(CrossSectionContainer, self).__init__(title, parent=parent)

        self.cross_section = cross_section


class CrossSectionView(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CrossSectionView, self).__init__(parent)

        self.cross_sections = QtGui.QListWidget(self)
        # self.description = QtGui.QLabel(self)
        self.description = QtGui.QTextEdit()
        self.description.setReadOnly(True)

        v_layout = QtGui.QVBoxLayout()
        v_layout.addWidget(self.cross_sections)
        v_layout.addWidget(self.description)

        self.setLayout(v_layout)

        self.cross_sections.setDragEnabled(True)

        self.cross_sections.itemClicked.connect(self.show_info)

    def clear_cross_sections(self):
        self.cross_sections.clear()

    def file_selected(self, filename):
        self.file_selected_action(filename, True)

    def dir_selected(self, filename):
        self.file_selected_action(filename, False)

    def file_selected_action(self, filename, clear):
        filename = str(filename)

        module_name = inspect.getmodulename(filename)
        sub_packages = '/'.join(
            filename[filename.index('ionics/')+len('ionics/'):].split('/')[:-1]
        ).replace('/', '.')

        exec('from %s import %s' % (sub_packages, module_name))

        try:
            cross_sections = eval(module_name + '.cross_sections')
        except AttributeError:
            # QtGui.QMessageBox.warning(
            #     self,
            #     'No cross sections found',
            #     "File %s does not expose any cross sections via 'cross_sections'" % filename
            # )
            return

        if clear:
            self.cross_sections.clear()
        for cs in cross_sections:
            self.cross_sections.addItem(CrossSectionContainer(cs.__name__, cs))

    def show_info(self, item):
        self.description.setText(item.cross_section.__doc__)
