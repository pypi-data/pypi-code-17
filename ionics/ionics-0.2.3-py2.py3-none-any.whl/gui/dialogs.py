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

import numpy

from . import pyqt45

Widgets = pyqt45.Widgets


class CrossSectionPlotParametersDialog(Widgets.QDialog):
    def __init__(self, cross_section, parent=None):
        super(CrossSectionPlotParametersDialog, self).__init__(parent)

        v_layout = Widgets.QVBoxLayout()

        init_header = Widgets.QLabel()
        init_header.setText('Initialize cross section with the following parameters:')
        init_header.setStyleSheet('QLabel { text-decoration: underline; font-weight: bold; }')
        v_layout.addWidget(init_header)

        h_layout = Widgets.QHBoxLayout()
        # Do not include `self`.
        self.init_args = inspect.getargspec(cross_section.__init__).args[1:]
        try:
            defaults = list(inspect.getargspec(cross_section.__init__).defaults)
        except TypeError:  # No defaults (defaults == None).
            defaults = []
        defaults = [None for _ in range(len(self.init_args) - len(defaults))] + defaults
        for arg in self.init_args:
            label = Widgets.QLabel()
            label.setText(arg+' = ')

            input_field = Widgets.QLineEdit()
            default = defaults.pop(0)
            input_field.setText(default if default else '')
            setattr(self, arg+'_input', input_field)

            h_layout.addWidget(label)
            h_layout.addWidget(input_field)

        v_layout.addLayout(h_layout)

        init_doc = Widgets.QTextEdit()
        init_doc.setReadOnly(True)
        init_doc.setText(cross_section.__init__.__doc__)
        v_layout.addWidget(init_doc)

        v_layout.addSpacing(20)

        call_header = Widgets.QLabel()
        call_header.setText('Specify the range for the plot:')
        call_header.setStyleSheet('QLabel { text-decoration: underline; font-weight: bold; }')
        v_layout.addWidget(call_header)

        # Do not include `self`.
        self.call_args = inspect.getargspec(cross_section.__call__).args[1:]
        for arg in self.call_args:
            label_min = Widgets.QLabel()
            label_min.setText(arg+'_min')

            input_min = Widgets.QLineEdit()
            setattr(self, arg+'_input_min', input_min)

            label_max = Widgets.QLabel()
            label_max.setText(arg+'_max')

            input_max = Widgets.QLineEdit()
            setattr(self, arg+'_input_max', input_max)

            label_steps = Widgets.QLabel()
            label_steps.setText(arg+'_steps')

            input_steps = Widgets.QLineEdit()
            setattr(self, arg+'_input_steps', input_steps)

            scale_linear = Widgets.QRadioButton('linear')
            scale_log = Widgets.QRadioButton('log')
            scale_group = Widgets.QButtonGroup()
            scale_group.addButton(scale_linear)
            scale_group.addButton(scale_log)
            scale_group.setExclusive(True)
            setattr(self, arg+'_scale', scale_group)
            scale_group_view = Widgets.QGroupBox('scale:')
            scale_layout = Widgets.QVBoxLayout()
            scale_layout.addWidget(scale_linear)
            scale_layout.addWidget(scale_log)
            scale_group_view.setLayout(scale_layout)

            if arg == 'W':
                input_min.setText('0.1')
                input_max.setText('100')
                input_steps.setText('100')
                scale_log.setChecked(True)
            elif arg == 'T':
                input_min.setText('0')
                input_max.setText('2*pi')
                input_steps.setText('100')
                scale_linear.setChecked(True)

            h_layout = Widgets.QHBoxLayout()
            h_layout.addWidget(label_min)
            h_layout.addWidget(input_min)
            h_layout.addWidget(label_max)
            h_layout.addWidget(input_max)
            h_layout.addWidget(label_steps)
            h_layout.addWidget(input_steps)
            h_layout.addWidget(scale_group_view)

            v_layout.addLayout(h_layout)

        call_doc = Widgets.QTextEdit()
        call_doc.setReadOnly(True)
        call_doc.setText(cross_section.__call__.__doc__)
        v_layout.addWidget(call_doc)

        h_layout = Widgets.QHBoxLayout()
        h_layout.addStretch(1)
        ok_button = Widgets.QPushButton('ok')
        ok_button.clicked.connect(self.check_inputs)
        ok_button.setAutoDefault(True)
        # ok_button.setDefault(True)
        # ok_button.setStyleSheet("QPushButton:default { background-color: orange; } ")
        h_layout.addWidget(ok_button)
        cancel_button = Widgets.QPushButton('cancel')
        cancel_button.clicked.connect(self.reject)
        h_layout.addWidget(cancel_button)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def check_inputs(self):
        try:
            inputs = self.get_inputs()
        except (AttributeError, ValueError, TypeError, SyntaxError):
            Widgets.QMessageBox.warning(self, 'Invalid input', 'Please enter valid parameters.')
        else:
            if all(inputs['init']):
                self.accept()
            else:
                Widgets.QMessageBox.warning(
                    self,
                    'Missing input',
                    'Please fill all input parameter fields.'
                )

    def get_inputs(self):
        return {
            'init': [
                str(getattr(self, arg+'_input').text())
                for arg in self.init_args
            ],
            'call': [
                (
                    float(eval(str(getattr(self, arg+'_input_min').text()), {}, {'pi': numpy.pi})),
                    float(eval(str(getattr(self, arg+'_input_max').text()), {}, {'pi': numpy.pi})),
                    int(getattr(self, arg+'_input_steps').text()),
                    str(getattr(self, arg+'_scale').checkedButton().text())
                ) for arg in self.call_args
            ],
        }


class PlotCustomizationDialog(Widgets.QDialog):
    def __init__(self, parent=None):
        super(PlotCustomizationDialog, self).__init__(parent)

        self.input_dict = {}

        def create_title_label(title):
            title_label = Widgets.QLabel(title)
            title_label.setStyleSheet('QLabel { text-decoration: underline; font-weight: bold; }')
            return title_label

        def create_labelled_input_and_insert_into_layout(label_text):
            h_layout = Widgets.QHBoxLayout()
            label = Widgets.QLabel(label_text+':')
            line_input = Widgets.QLineEdit()
            setattr(self, label_text+'_input', line_input)
            self.input_dict[label_text] = line_input
            h_layout.addWidget(label)
            h_layout.addWidget(line_input)
            return h_layout

        def create_widget_and_set_layout(layout):
            widget = Widgets.QWidget()
            widget.setLayout(layout)
            return widget

        v_layout = Widgets.QVBoxLayout()

        w_v_layout = Widgets.QVBoxLayout()
        w_v_layout.addWidget(create_title_label('Title'))
        w_v_layout.addLayout(create_labelled_input_and_insert_into_layout('title'))
        v_layout.addWidget(create_widget_and_set_layout(w_v_layout))

        w_v_layout = Widgets.QVBoxLayout()
        w_v_layout.addWidget(create_title_label('Axes labels'))
        w_h_layout = Widgets.QHBoxLayout()
        w_h_layout.addLayout(create_labelled_input_and_insert_into_layout('x-axis'))
        w_h_layout.addLayout(create_labelled_input_and_insert_into_layout('y-axis'))
        w_h_layout.addLayout(create_labelled_input_and_insert_into_layout('z-axis'))
        w_h_layout.addStretch(1)
        w_v_layout.addLayout(w_h_layout)
        v_layout.addWidget(create_widget_and_set_layout(w_v_layout))

        h_layout = Widgets.QHBoxLayout()
        h_layout.addStretch(1)
        ok_button = Widgets.QPushButton('ok')
        ok_button.clicked.connect(self.check_inputs)
        ok_button.setAutoDefault(True)
        h_layout.addWidget(ok_button)
        cancel_button = Widgets.QPushButton('cancel')
        cancel_button.clicked.connect(self.reject)
        h_layout.addWidget(cancel_button)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def check_inputs(self):
        self.accept()

    def get_inputs(self):
        return {k: str(v.text()) for k, v in iter(self.input_dict.items())}
