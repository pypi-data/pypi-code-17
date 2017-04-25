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

import types

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm
import matplotlib.patches as mpatches
from PyQt4 import QtGui, QtCore

from .dialogs import CrossSectionPlotParametersDialog as ParameterDialog
from .dialogs import PlotCustomizationDialog as CustomizationDialog
from .plots import arange_input
from .plots import generate_data_sdcs, generate_data_ddcs


class PlotView(QtGui.QWidget):
    marker_list = list(reversed(['bo', 'rx', 'gs', 'y^', 'm*']))

    def __init__(self, cross_section_view, parent=None):
        super(PlotView, self).__init__(parent)

        self.cross_section_view = cross_section_view
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        def add_scales(ax):
            lin_button = QtGui.QRadioButton('linear')
            log_button = QtGui.QRadioButton('log')
            log_button.setChecked(True)
            scale_group = QtGui.QButtonGroup()
            scale_group.addButton(lin_button)
            scale_group.addButton(log_button)
            scale_group.setExclusive(True)
            setattr(self, ax+'_scale', scale_group)
            layout = QtGui.QVBoxLayout()
            layout.addWidget(lin_button)
            layout.addWidget(log_button)
            scale_group_view = QtGui.QGroupBox(ax+'-scale')
            scale_group_view.setLayout(layout)
            return scale_group_view

        scale_layout = QtGui.QHBoxLayout()
        scale_layout.addWidget(add_scales('x'), 0)
        scale_layout.addWidget(add_scales('y'), 0)
        scale_layout.addWidget(add_scales('z'), 0)
        # scale_layout.addStretch(1)

        below_plot_layout = QtGui.QHBoxLayout()
        below_plot_layout.addLayout(scale_layout)
        below_plot_layout.addStretch(1)

        customize_button = QtGui.QPushButton('customize plot')
        customize_button.clicked.connect(self.customize_canvas)
        below_plot_layout.addWidget(customize_button)

        save_button = QtGui.QPushButton('save')
        save_button.clicked.connect(self.save_canvas)
        below_plot_layout.addWidget(save_button)

        clear_button = QtGui.QPushButton('clear')
        clear_button.clicked.connect(self.clear_canvas)
        below_plot_layout.addWidget(clear_button)

        delete_button = QtGui.QPushButton('delete')
        delete_button.clicked.connect(self.delete_canvas)
        below_plot_layout.addWidget(delete_button)

        v_layout = QtGui.QVBoxLayout()
        v_layout.addWidget(self.canvas)
        v_layout.addLayout(below_plot_layout)

        self.x_scale.buttonClicked.connect(self.change_x_scale)
        self.y_scale.buttonClicked.connect(self.change_y_scale)
        self.z_scale.buttonClicked.connect(self.change_z_scale)

        self.marker_list = [m for m in PlotView.marker_list]

        self.handles = []
        self.labels = []

        self.setAcceptDrops(True)

        self.canvas.setMinimumSize(QtCore.QSize(800, 800))

        def heightForWidth(self, w):
            return w

        self.canvas.heightForWidth = types.MethodType(heightForWidth, self.canvas)

        self.setLayout(v_layout)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()
        cross_section_cls = self.cross_section_view.cross_sections.currentItem().cross_section

        # plot cross section here
        dialog = ParameterDialog(cross_section_cls)
        if dialog.exec_():
            parameters = dialog.get_inputs()
        else:
            return

        try:
            cross_section = cross_section_cls(*parameters['init'])
        except ValueError:
            QtGui.QMessageBox.warning(
                self,
                'Invalid __init__ parameters',
                'Please enter valid parameters for the initialization of the cross section.'
            )
            return

        parameters['call'] = [
            arange_input(x[0], x[1], x[2], scale=x[3]) for x in parameters['call']
        ]

        pars = parameters['call']
        if len(pars) == 1:
            cs_data = generate_data_sdcs(pars[0], cross_section)
            self.plot_sdcs(pars[0], cs_data, cross_section)
        elif len(pars) == 2:
            cs_data = generate_data_ddcs(pars[0], pars[1], cross_section)
            self.plot_ddcs(pars[0], pars[1], cs_data)

    def plot_sdcs(self, x, y, cross_section):
        marker = self.marker_list.pop()
        self.axes.plot(x, y, marker, label=cross_section.__class__.__name__)

        self.axes.set_ylabel('sdcs')
        self.axes.set_xscale(str(self.x_scale.checkedButton().text()))
        self.axes.set_yscale(str(self.x_scale.checkedButton().text()))

        self.handles.append(
            mpatches.Patch(color=marker[0], label=cross_section.__class__.__name__)
        )
        self.labels.append(cross_section.__class__.__name__)
        self.figure.legend(handles=self.handles, labels=self.labels)

        self.canvas.draw()

    def plot_ddcs(self, x, y, z):
        self.clear_canvas()

        z_scale = str(self.z_scale.checkedButton().text())
        if z_scale == 'log':
            plot = self.axes.pcolor(x, y, z, norm=LogNorm(vmin=z.min(), vmax=z.max()))
        elif z_scale == 'linear':
            plot = self.axes.pcolor(x, y, z)
        else:
            raise ValueError('invalid scale: %s' % z_scale)

        cbar = self.figure.colorbar(plot)
        cbar.ax.set_ylabel('ddcs')
        setattr(self.axes, 'set_zlabel', cbar.ax.set_ylabel)
        self.axes.set_xscale(str(self.x_scale.checkedButton().text()))
        self.axes.set_yscale(str(self.x_scale.checkedButton().text()))

        self.canvas.draw()

    def change_x_scale(self, button):
        self.axes.set_xscale(str(button.text()))
        self.canvas.draw()

    def change_y_scale(self, button):
        self.axes.set_yscale(str(button.text()))
        self.canvas.draw()

    def change_z_scale(self, button):
        pass

    def customize_canvas(self):
        input_func_map = {
            'title': self.figure.suptitle,
            'x-axis': self.axes.set_xlabel,
            'y-axis': self.axes.set_ylabel,
        }
        try:
            input_func_map['z-axis'] = self.axes.set_zlabel
        except AttributeError:
            input_func_map['z-axis'] = None
        dialog = CustomizationDialog(self)
        if dialog.exec_():
            inputs = dialog.get_inputs()
            for k, v in inputs.iteritems():
                if input_func_map[k] and v:
                    input_func_map[k](v)
            self.canvas.draw()

    def save_canvas(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(
            self,
            'Save plot',
            filter='Images (*.png *.jpg *.jpeg *.eps *.ps)'
        ))
        if filename:
            if '.' not in filename:
                filename += '.png'
            self.figure.savefig(filename)

    def clear_canvas(self):
        self.figure.clear()
        self.handles = []
        self.labels = []
        self.axes = self.figure.add_subplot(111)
        self.canvas.draw()
        self.marker_list = [m for m in PlotView.marker_list]

    def delete_canvas(self):
        self.hide()
