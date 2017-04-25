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

from PyQt4 import QtGui

from .mainwidget import MainWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        main_widget = MainWidget(self)
        self.setCentralWidget(main_widget)

        menubar = self.menuBar()
        help_menu = menubar.addMenu('Help')
        about_action = QtGui.QAction('About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        license_action = QtGui.QAction('License', self)
        license_action.triggered.connect(self._show_license_info)
        help_menu.addAction(license_action)

    def _show_about(self):
        QtGui.QMessageBox.information(
            self,
            'About ionics',
            '`ionics` is a software which models various ionization cross sections.'
        )

    def _show_license_info(self):
        QtGui.QMessageBox.information(
            self,
            'License information',
            '`ionics` is a software which models various ionization cross sections.\n'
            'Copyright (C) 2017  Dominik Vilsmeier\n'
            '\n'
            'This program is free software: you can redistribute it and/or modify\n'
            'it under the terms of the GNU General Public License as published by\n'
            'the Free Software Foundation, either version 3 of the License, or\n'
            '(at your option) any later version.\n'
            '\n'
            'This program is distributed in the hope that it will be useful,\n'
            'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
            'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
            'GNU General Public License for more details.\n'
            '\n'
            'You should have received a copy of the GNU General Public License\n'
            'along with this program.  If not, see <http://www.gnu.org/licenses/>.'
        )
