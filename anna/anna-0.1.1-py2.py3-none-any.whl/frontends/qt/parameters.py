# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

# noinspection PyPackageRequirements,PyUnresolvedReferences
from PyQt4 import QtGui

from anna.adaptors import ConfigurationAdaptor as Adaptor
from anna.exceptions import InvalidRepresentationError
import anna.parameters as parameters


class InvalidInputError(Exception):
    pass


class ParameterInput(QtGui.QWidget):
    """
    Base class for input fields. The ``PEER`` class attribute should be set to
    the corresponding parameter type.
    """

    PEER = parameters.Parameter

    def __init__(self, parameter, parent=None):
        """
        Instantiate the input field with a corresponding parameter.

        Parameters
        ----------
        parameter : :py:class:`Parameter`
        parent : QWidget or None
        """
        super(ParameterInput, self).__init__(parent)

        self._parameter = parameter
        self.setToolTip(parameter.info or 'No information available.')

    @property
    def name(self):
        """
        Retrieve the name of the corresponding parameter

        Returns
        -------
        name : unicode
        """
        return self._parameter.name

    @property
    def text(self):
        """
        Retrieve the text representation of this input field. This method should be overridden
        in base classes as appropriate.

        Returns
        -------
        text : unicode
            An empty string
        """
        return ''

    @text.setter
    def text(self, value):
        pass

    @property
    def meta(self):
        """
        Retrieve the meta representation of this input field. This method should be overridden
        in base classes as appropriate.

        Returns
        -------
        meta : dict
            An empty dict
        """
        return {}

    @meta.setter
    def meta(self, value):
        pass

    @property
    def needs_to_be_dumped(self):
        """
        Check if the input field's value needs to be dumped. A field doesn't need to be dumped if
        its corresponding parameter has a default value and the input field contains
        the exact same value.

        Returns
        -------
        needs_to_be_dumped : bool
        """
        return not ((self._parameter.is_optional and not self.text)
                    or
                    (self._parameter.is_expert and
                     self._parameter.convert_representation(self.text) == self._parameter.default))

    def as_adaptor_element(self):
        """
        Convert the input field to an instance of :py:class:`ConfigurationAdaptor.Element`.

        Returns
        -------
        adaptor_element : :py:class:`ConfigurationAdaptor.Element`
        """
        try:
            self._parameter.validate_representation(self.text, self.meta)
        except InvalidRepresentationError as err:
            raise InvalidInputError('%s: %s' % (self._parameter.name, six.text_type(err)))
        meta = self.meta if self._parameter.info is None \
            else dict(self.meta, info=self._parameter.info)
        return Adaptor.Element(self._parameter.name, self.text, meta)

    def load_from_adaptor_element(self, element):
        """
        Fill this input field from the contents of an instance of
        :py:class:`ConfigurationAdaptor.Element`.

        Parameters
        ----------
        element : :py:class:`ConfigurationAdaptor.Element`
        """
        self.text = element.text
        self.meta = element.meta

    def load_default(self):
        """
        Fill this input field with the default value of the corresponding parameters if
        available or leave it empty otherwise.
        """
        self._set_default(self._parameter)

    def _set_default(self, parameter):
        """
        Fill the input field with the default value of the given parameter (if available).
        Otherwise leave it empty.

        Parameters
        ----------
        parameter : :class:`Parameter` derived class
        """
        pass


class BoolInput(ParameterInput):
    PEER = parameters.BoolParameter

    def __init__(self, parameter, parent=None):
        super(BoolInput, self).__init__(parameter, parent)

        self._check_box = QtGui.QCheckBox()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._check_box)
        layout.addStretch(1)
        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        return parameters.BoolParameter.true if self._check_box.isChecked() \
            else parameters.BoolParameter.false

    @text.setter
    def text(self, value):
        self._check_box.setChecked(value == parameters.BoolParameter.true)

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._check_box.setChecked(parameter.default)


class IntegerInput(ParameterInput):
    PEER = parameters.IntegerParameter

    def __init__(self, parameter, parent=None):
        super(IntegerInput, self).__init__(parameter, parent)

        self._line_edit = QtGui.QLineEdit()
        self._line_edit.setPlaceholderText('integer')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)
        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(six.text_type(parameter.default))


class NumberInput(ParameterInput):
    PEER = parameters.NumberParameter

    def __init__(self, parameter, parent=None):
        super(NumberInput, self).__init__(parameter, parent)

        self._line_edit = QtGui.QLineEdit()
        self._line_edit.setPlaceholderText('number')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)
        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(six.text_type(parameter.default))


class PhysicalQuantityInput(ParameterInput):
    PEER = parameters.PhysicalQuantityParameter

    def __init__(self, parameter, parent=None):
        super(PhysicalQuantityInput, self).__init__(parameter, parent)

        self.magnitude = QtGui.QLineEdit()
        self.magnitude.setPlaceholderText('magnitude')

        self.unit = QtGui.QLineEdit()
        self.unit.setPlaceholderText('unit')

        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(QtGui.QLabel(parameter.name))
        h_layout.addWidget(self.magnitude, 1)
        h_layout.addWidget(self.unit)
        self.setLayout(h_layout)

    @property
    def text(self):
        return six.text_type(self.magnitude.text()).strip()

    @text.setter
    def text(self, value):
        self.magnitude.setText(value)

    @property
    def meta(self):
        return {'unit': six.text_type(self.unit.text()).strip()}

    @meta.setter
    def meta(self, value):
        self.unit.setText(value['unit'])

    @property
    def needs_to_be_dumped(self):
        return not self._parameter.is_optional


class StringInput(ParameterInput):
    PEER = parameters.StringParameter

    def __init__(self, parameter, parent=None):
        super(StringInput, self).__init__(parameter, parent)

        self._line_edit = QtGui.QLineEdit()
        self._line_edit.setPlaceholderText('string')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)

        if 'file' in parameter.name.lower():
            open_file_push_button = QtGui.QPushButton('Open file')

            def set_open_filename():
                filename = six.text_type(QtGui.QFileDialog.getOpenFileName())
                if filename:
                    self.text = filename

            # noinspection PyUnresolvedReferences
            open_file_push_button.clicked.connect(set_open_filename)
            layout.addWidget(open_file_push_button)

            save_file_push_button = QtGui.QPushButton('Save file')

            def set_save_filename():
                filename = six.text_type(QtGui.QFileDialog.getSaveFileName())
                if filename:
                    self.text = filename

            # noinspection PyUnresolvedReferences
            save_file_push_button.clicked.connect(set_save_filename)
            layout.addWidget(save_file_push_button)

        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(parameter.default)


class ChoiceInput(ParameterInput):
    PEER = parameters.ChoiceParameter

    def __init__(self, parameter, parent=None):
        super(ChoiceInput, self).__init__(parameter, parent)

        self._choices = QtGui.QComboBox()
        for option in parameter.options:
            self._choices.addItem(option)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._choices)
        layout.addStretch(1)
        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        return six.text_type(self._choices.currentText())

    @text.setter
    def text(self, value):
        if value in self._parameter.options:
            self._choices.setCurrentIndex(self._parameter.options.index(value))

    def _set_default(self, parameter):
        if parameter.is_expert:
            self.text = parameter.default


class GroupInput(ParameterInput):
    PEER = parameters.ParameterGroup

    def __init__(self, parameter_group, parent=None):
        super(GroupInput, self).__init__(parameter_group, parent)

        names = QtGui.QComboBox()
        self.input_fields = QtGui.QStackedWidget()
        for option in parameter_group:
            names.addItem(option.name)
            input_field = from_type(option.parameter)
            # Remove name label from input field as the name is already present in the combo box.
            input_field.layout().takeAt(0)
            self.input_fields.addWidget(input_field)

        def select_option(index):
            self.input_fields.setCurrentIndex(index)

        # noinspection PyUnresolvedReferences
        names.currentIndexChanged.connect(select_option)
        names.setCurrentIndex(0)

        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(names)
        h_layout.addWidget(self.input_fields)
        self.setLayout(h_layout)

    @property
    def text(self):
        return self.input_fields.currentWidget().text

    @text.setter
    def text(self, value):
        self.input_fields.currentWidget().text = value

    @property
    def meta(self):
        return self.input_fields.currentWidget().meta

    @meta.setter
    def meta(self, value):
        self.input_fields.currentWidget().meta = value


class VectorInput(ParameterInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(VectorInput, self).__init__(parameter, parent)

        self._line_edit = QtGui.QLineEdit()
        self._line_edit.setPlaceholderText('vector (separate elements with commas)')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)
        self.setLayout(layout)
        self._set_default(parameter)

    @property
    def text(self):
        text_repr = six.text_type(self._line_edit.text()).strip()
        if not text_repr.startswith('['):
            text_repr = '[ ' + text_repr
        if not text_repr.endswith(']'):
            text_repr += ' ]'
        return text_repr

    @text.setter
    def text(self, value):
        if value.startswith('['):
            value = value[1:]
        if value.endswith(']'):
            value = value[:-1]
        value = value.strip()
        self._line_edit.setText(value)

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(
                ', '.join(map(
                    six.text_type,
                    parameter.default
                ))
            )


class DupletInput(VectorInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(DupletInput, self).__init__(parameter, parent)
        self._line_edit.setPlaceholderText('2-tuple (separate elements with commas)')


class TripletInput(VectorInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(TripletInput, self).__init__(parameter, parent)
        self._line_edit.setPlaceholderText('3-tuple (separate elements with commas)')


class PhysicalVectorQuantityInput(ParameterInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(PhysicalVectorQuantityInput, self).__init__(parameter, parent)

        self.vector = QtGui.QLineEdit()
        self.vector.setPlaceholderText('vector (separate elements with commas)')

        self.unit = QtGui.QLineEdit()
        self.unit.setPlaceholderText('unit')

        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(QtGui.QLabel(parameter.name))
        h_layout.addWidget(self.vector, 1)
        h_layout.addWidget(self.unit)
        self.setLayout(h_layout)

    @property
    def text(self):
        text_repr = six.text_type(self.vector.text()).strip()
        if not text_repr.startswith('['):
            text_repr = '[ ' + text_repr
        if not text_repr.endswith(']'):
            text_repr += ' ]'
        return text_repr

    @text.setter
    def text(self, value):
        if value.startswith('['):
            value = value[1:]
        if value.endswith(']'):
            value = value[:-1]
        value = value.strip()
        self.vector.setText(value)

    @property
    def meta(self):
        return {'unit': six.text_type(self.unit.text()).strip()}

    @meta.setter
    def meta(self, value):
        self.unit.setText(value['unit'])

    @property
    def needs_to_be_dumped(self):
        return not self._parameter.is_optional


class PhysicalDupletInput(PhysicalVectorQuantityInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(PhysicalDupletInput, self).__init__(parameter, parent)
        self.vector.setPlaceholderText('2-tuple (separate elements with commas)')


class PhysicalTripletInput(PhysicalVectorQuantityInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(PhysicalTripletInput, self).__init__(parameter, parent)
        self.vector.setPlaceholderText('3-tuple (separate elements with commas)')


def from_type(parameter):
    """
    Retrieve the appropriate input field class for the given parameter.

    Parameters
    ----------
    parameter : :py:class:`Parameter`

    Returns
    -------
    input_field_cls : :py:class:`ParameterInput`
        The input field class corresponding to the given parameter's type.
    """
    # An AwareParameter can host an ActionParameter so we need to check for AwareParameters first.
    if isinstance(parameter, parameters.AwareParameter):
        parameter = parameter.parameter
    if isinstance(parameter, parameters.ActionParameter):
        parameter = parameter.parameter

    inputs = filter(
        lambda obj: isinstance(obj, type) and issubclass(obj, ParameterInput),
        globals().values()
    )

    if issubclass(type(parameter), parameters._TripletParameterTemplate):
        if issubclass(parameter._element_type, parameters.PhysicalQuantityParameter):
            return PhysicalTripletInput(parameter)
        else:
            return TripletInput(parameter)
    elif issubclass(type(parameter), parameters._DupletParameterTemplate):
        if issubclass(parameter._element_type, parameters.PhysicalQuantityParameter):
            return PhysicalDupletInput(parameter)
        else:
            return DupletInput(parameter)
    elif issubclass(type(parameter), parameters._VectorParameterTemplate):
        if issubclass(parameter._element_type, parameters.PhysicalQuantityParameter):
            return PhysicalVectorQuantityInput(parameter)
        else:
            return VectorInput(parameter)

    try:
        # Needs to use type rather than isinstance because some parameter types subclass others.
        input_cls = list(filter(lambda x: type(parameter) == x.PEER, inputs))[0]
    except IndexError:
        raise TypeError('No input widget for parameter of type `%s`' % type(parameter))
    return input_cls(parameter)
