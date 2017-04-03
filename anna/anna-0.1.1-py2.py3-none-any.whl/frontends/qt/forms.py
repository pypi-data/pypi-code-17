# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# noinspection PyPackageRequirements,PyUnresolvedReferences
from PyQt4 import QtGui

from anna.adaptors import ConfigurationAdaptor as Adaptor
from anna.adaptors import JSONAdaptor, XMLAdaptor
from anna.exceptions import InvalidPathError
from anna.parameters import ActionParameter, AwareParameter
from anna.frontends.qt.parameters import from_type


class ParameterForm(QtGui.QWidget):
    """QWidget that contains input forms for a list of parameters."""

    def __init__(self, parameters, parent=None):
        """
        Initialize the form with input fields for the given parameters.

        Parameters
        ----------
        parameters : list
            List of parameters
        parent : QWidget or None
        """
        super(ParameterForm, self).__init__(parent)

        self._input_fields = {}

        if parameters:
            nonexpert_parameters = filter(
                lambda p: not (p.is_expert or p.is_optional),
                parameters
            )
            expert_parameters = filter(
                lambda p: p.is_expert or p.is_optional,
                parameters
            )

            v_layout = QtGui.QVBoxLayout()
            v_layout.addWidget(QtGui.QLabel('<u>Parameters:</u>'))
            v_layout.addLayout(self._layout_parameters(nonexpert_parameters))

            if expert_parameters:
                advanced_panel = QtGui.QWidget()
                advanced_panel.setLayout(self._layout_parameters(expert_parameters))
                advanced_panel.hide()

                # Could use QToolButton instead (for having an arrow next to the text).
                show_advanced_button = QtGui.QPushButton('> Advanced options')
                show_advanced_button.setStyleSheet(
                    'QPushButton { border: none; text-decoration: underline; }'
                )
                show_advanced_button.setFlat(True)

                def show_advanced(_):
                    if advanced_panel.isVisible():
                        advanced_panel.hide()
                    else:
                        advanced_panel.show()

                # noinspection PyUnresolvedReferences
                show_advanced_button.clicked.connect(show_advanced)

                button_layout = QtGui.QHBoxLayout()
                button_layout.addWidget(show_advanced_button)
                button_layout.addStretch(1)

                v_layout.addLayout(button_layout)
                v_layout.addWidget(advanced_panel)

            self.setLayout(v_layout)

    def __iter__(self):
        return iter(self.input_fields.items())

    def dump_as_xml(self):
        """"
        Dump the for as an xml adaptor.

        Returns
        -------
        config : ``XMLAdaptor``
        """
        return self.dump_as('xml')

    def dump_as_json(self):
        """
        Dump the for as an json adaptor.

        Returns
        -------
        config : ``JSONAdaptor``
        """
        return self.dump_as('json')

    def dump_as(self, format_):
        """
        Dump the form as a configuration adaptor.

        Parameters
        ----------
        format_ : unicode
            Specifies the format in which the content should be saved ("xml" or "json").

        Returns
        -------
        config : :py:class:`ConfigurationAdaptor` derived class
        """
        if format_ == 'xml':
            config = XMLAdaptor()
        elif format_ == 'json':
            config = JSONAdaptor()
        else:
            raise ValueError(
                'format_ must be either "xml" or "json" (got "%s" instead)'
                % format_
            )
        for path, input_field in iter(self._input_fields.items()):
            if input_field.needs_to_be_dumped:
                config.insert_element(path, input_field.as_adaptor_element())
        return config

    def load_from_source(self, configuration):
        """
        Fill the form with values from the given configuration source.

        Parameters
        ----------
        configuration : :py:class:`ConfigurationAdaptor`
        """
        for path, input_field in iter(self._input_fields.items()):
            try:
                input_field.load_from_adaptor_element(configuration.get_element(path))
            except InvalidPathError:
                input_field.load_default()

    def _layout_parameters(self, parameters):
        layout = QtGui.QVBoxLayout()
        for parameter in parameters:
            # An AwareParameter can host an ActionParameter so we need to check for
            # AwareParameters first.
            derived_parameter = parameter
            if isinstance(parameter, AwareParameter):
                derived_parameter = parameter.parameter
            if isinstance(parameter, ActionParameter):
                derived_parameter = derived_parameter.parameter

            input_field = from_type(derived_parameter)
            self._input_fields[Adaptor.join_paths(parameter.path, input_field.name)] = input_field
            layout.addWidget(input_field)

        return layout
