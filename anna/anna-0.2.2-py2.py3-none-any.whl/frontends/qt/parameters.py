# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os.path
import textwrap

import numpy
import six

from anna.adaptors import ConfigurationAdaptor as Adaptor
from anna.adaptors import JSONAdaptor, XMLAdaptor
from anna.exceptions import InvalidPathError, RepresentationError, SpecificationError
from anna.input import Unit
import anna.parameters as parameters
from . import pyqt45

QtCore = pyqt45.QtCore
QtGui = pyqt45.QtGui
Widgets = pyqt45.Widgets


# noinspection PyOldStyleClasses
class InvalidInputError(Exception):
    def __init__(self, message, origin=None):
        super(InvalidInputError, self).__init__(message)
        self.origin = origin


class ParameterInput(Widgets.QWidget):
    """
    Base class for input fields. The ``PEER`` class attribute should be set to
    the corresponding parameter type.
    """

    text_modified = QtCore.pyqtSignal(six.text_type)
    meta_modified = QtCore.pyqtSignal()

    PEER = parameters.Parameter
    TOOLTIP_CHAR_WIDTH = 79
    NO_INFO_AVAILABLE = 'No information available.'
    INFO_ICON_PATH = 'icons/parameter_info.png'
    INFO_BUTTON_SIZE = (24, 24)

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
        self._info = parameter.info or self.NO_INFO_AVAILABLE
        self.setToolTip(textwrap.fill(self._info, self.TOOLTIP_CHAR_WIDTH))

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
        def compare_values_equal(v1, v2):
            if isinstance(v1, numpy.ndarray) and isinstance(v2, numpy.ndarray):
                return numpy.all(v1 == v2)
            elif isinstance(v1, numpy.ndarray):
                return numpy.all(v1 == numpy.array(v2))
            elif isinstance(v2, numpy.ndarray):
                return numpy.all(numpy.array(v1) == v2)
            else:
                return v1 == v2

        return not ((
                        self._parameter.is_optional
                        and not self.text
                    )
                    or (
                        self._parameter.is_expert
                        and not self.text
                    )
                    or (
                        self._parameter.is_expert
                        and self.text
                        and compare_values_equal(
                            self._parameter.load_from_representation(self.text, self.meta),
                            self._parameter.default
                        )
                    ))

    def as_adaptor_element(self):
        """
        Convert the input field to an instance of :py:class:`ConfigurationAdaptor.Element`.

        Returns
        -------
        adaptor_element : :py:class:`ConfigurationAdaptor.Element`
        """
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

    def validate_input(self):
        """
        Validate the given input for this field.
        
        Returns
        -------
        None
            If the given input is valid.
        
        Raises
        ------
        InvalidInputError
            If the given input is invalid.
        """
        if not self.text:
            return None
        try:
            self._parameter.validate_representation(self.text, self.meta)
            self._parameter.validate_specification(self.text, self.meta)
        except SpecificationError as err:
            if isinstance(self._parameter, parameters.AwareParameter):
                path = Adaptor.join_paths(self._parameter.path, self._parameter.name)
            else:
                path = self._parameter.name
            raise InvalidInputError('%s: %s' % (path, err.reason), self)
        return None

    def _set_default(self, parameter):
        """
        Fill the input field with the default value of the given parameter (if available).
        Otherwise leave it empty.

        Parameters
        ----------
        parameter : :class:`Parameter` derived class
        """
        pass

    def _set_info_button(self):
        """
        Insert an info button with the info text of the input field's parameter in the input
        field's layout. 
        """
        self.layout().insertWidget(0, self._setup_info_button())

    def _setup_info_button(self):
        """
        Set up an info button with the info text of the input field's parameter.
        """
        info_button = Widgets.QPushButton(
            QtGui.QIcon(os.path.join(os.path.split(__file__)[0], self.INFO_ICON_PATH)), ''
        )
        info_button.setStyleSheet('QPushButton { border: none; }')
        info_button.setFlat(True)
        info_button.setFixedSize(*self.INFO_BUTTON_SIZE)
        info_button.setToolTip(self._info)

        def show_info():
            Widgets.QMessageBox.information(self, self._parameter.name, self._info)

        # noinspection PyUnresolvedReferences
        info_button.clicked.connect(show_info)

        return info_button


class BoolInput(ParameterInput):
    PEER = parameters.BoolParameter

    def __init__(self, parameter, parent=None):
        super(BoolInput, self).__init__(parameter, parent)

        self._check_box = Widgets.QCheckBox()

        def trigger_text_modified(_):
            self.text_modified.emit(self.text)

        # noinspection PyUnresolvedReferences
        self._check_box.stateChanged.connect(trigger_text_modified)

        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self._check_box)
        layout.addStretch(1)
        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

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

        self._line_edit = Widgets.QLineEdit()
        self._line_edit.setPlaceholderText('integer')
        # noinspection PyUnresolvedReferences
        self._line_edit.textChanged.connect(self.text_modified.emit)

        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)
        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(IntegerInput, self).setFocus()
        self._line_edit.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(six.text_type(parameter.default))
        elif parameter.for_example is not None:
            self._line_edit.setText(six.text_type(parameter.for_example))


class NumberInput(ParameterInput):
    PEER = parameters.NumberParameter

    def __init__(self, parameter, parent=None):
        super(NumberInput, self).__init__(parameter, parent)

        self._line_edit = Widgets.QLineEdit()
        self._line_edit.setPlaceholderText('number')
        # noinspection PyUnresolvedReferences
        self._line_edit.textChanged.connect(self.text_modified.emit)

        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)
        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(NumberInput, self).setFocus()
        self._line_edit.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(six.text_type(parameter.default))
        elif parameter.for_example is not None:
            self._line_edit.setText(six.text_type(parameter.for_example))


class PhysicalQuantityInput(ParameterInput):
    PEER = parameters.PhysicalQuantityParameter

    meta_modified = QtCore.pyqtSignal(int)

    def __init__(self, parameter, parent=None):
        super(PhysicalQuantityInput, self).__init__(parameter, parent)

        self.magnitude = Widgets.QLineEdit()
        self.magnitude.setPlaceholderText('magnitude')
        # noinspection PyUnresolvedReferences
        self.magnitude.textChanged.connect(self.text_modified.emit)

        self.unit = self.setup_unit_field(parameter)
        # noinspection PyUnresolvedReferences
        self.unit.currentIndexChanged.connect(self.meta_modified.emit)

        h_layout = Widgets.QHBoxLayout()
        h_layout.addWidget(Widgets.QLabel(parameter.name))
        h_layout.addWidget(self.magnitude, 1)
        h_layout.addWidget(self.unit)
        self.setLayout(h_layout)

        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        return six.text_type(self.magnitude.text()).strip()

    @text.setter
    def text(self, value):
        self.magnitude.setText(value)

    @property
    def meta(self):
        return {'unit': self.get_unit_from_field(self.unit)}

    @meta.setter
    def meta(self, value):
        self.set_unit_on_field(self.unit, value['unit'], self._parameter)

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(PhysicalQuantityInput, self).setFocus()
        self.magnitude.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self.text = six.text_type(parameter.default)
            self.meta = {'unit': parameter.unit}
        elif parameter.for_example is not None:
            self.text = six.text_type(parameter.for_example)
            self.meta = {'unit': parameter.unit}

    @staticmethod
    def get_unit_from_field(field):
        return six.text_type(field.currentText()).strip()

    @staticmethod
    def set_unit_on_field(field, unit, parameter):
        # noinspection PyUnresolvedReferences
        index_per_unit = {
            six.text_type(field.itemText(index)): index
            for index in six.moves.range(field.count())
        }
        try:
            field.setCurrentIndex(index_per_unit[unit])
        except KeyError:
            if isinstance(parameter, parameters.AwareParameter):
                path = Adaptor.join_paths(parameter.path, parameter.name)
            else:
                path = parameter.name
            raise InvalidInputError(
                'Invalid unit "{0}" for parameter {1} which has dimension {2}'.format(
                    unit, path, Unit.dimension(parameter.unit)
                )
            )

    @staticmethod
    def setup_unit_field(parameter):
        unit_field = Widgets.QComboBox()
        units = Unit._units_per_dimension[
            Unit.dimension(parameter.unit)
        ]
        for unit in units:
            unit_field.addItem(unit)
        return unit_field


class StringInput(ParameterInput):
    PEER = parameters.StringParameter

    def __init__(self, parameter, parent=None):
        super(StringInput, self).__init__(parameter, parent)

        self._line_edit = Widgets.QLineEdit()
        self._line_edit.setPlaceholderText('string')
        # noinspection PyUnresolvedReferences
        self._line_edit.textChanged.connect(self.text_modified.emit)

        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self._line_edit, 1)

        if 'file' in parameter.name.lower():
            open_file_push_button = Widgets.QPushButton('Open file')

            def set_open_filename():
                filename = six.text_type(pyqt45.getOpenFileName())
                if filename:
                    self.text = filename

            # noinspection PyUnresolvedReferences
            open_file_push_button.clicked.connect(set_open_filename)
            layout.addWidget(open_file_push_button)

            save_file_push_button = Widgets.QPushButton('Save file')

            def set_save_filename():
                filename = six.text_type(pyqt45.getSaveFileName())
                if filename:
                    self.text = filename

            # noinspection PyUnresolvedReferences
            save_file_push_button.clicked.connect(set_save_filename)
            layout.addWidget(save_file_push_button)

        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        return six.text_type(self._line_edit.text())

    @text.setter
    def text(self, value):
        self._line_edit.setText(value)

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(StringInput, self).setFocus()
        self._line_edit.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self._line_edit.setText(parameter.default)
        elif parameter.for_example is not None:
            self._line_edit.setText(parameter.for_example)


class ChoiceInput(ParameterInput):
    PEER = parameters.ChoiceParameter

    def __init__(self, parameter, parent=None):
        super(ChoiceInput, self).__init__(parameter, parent)

        self._choices = Widgets.QComboBox()
        for option in parameter.options:
            self._choices.addItem(option)
        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self._choices)
        layout.addStretch(1)
        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

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
        elif parameter.for_example is not None:
            self.text = parameter.for_example


class ComplementaryGroupInput(ParameterInput):
    PEER = parameters.ComplementaryParameterGroup

    def __init__(self, complementary_group, parent=None):
        super(ComplementaryGroupInput, self).__init__(complementary_group, parent)

        self._group = complementary_group
        self._last_activated = None

        # noinspection PyShadowingNames
        def new_checkbox_trigger(index):
            def trigger(state):
                self._member_activation_changed(index, state)
            return trigger

        # noinspection PyShadowingNames
        def new_member_modification_trigger(index):
            def trigger(*args):
                self._member_modified(index, *args)
            return trigger

        v_layout = Widgets.QVBoxLayout()

        line = Widgets.QFrame(flags=QtCore.Qt.Widget)
        line.setFrameShape(Widgets.QFrame.HLine)
        line.setFrameShadow(Widgets.QFrame.Sunken)
        v_layout.addWidget(line)

        h_layout = Widgets.QHBoxLayout()
        h_layout.addWidget(self._setup_info_button())
        h_layout.addWidget(Widgets.QLabel(self._group.name))
        h_layout.addStretch(1)
        v_layout.addLayout(h_layout)

        self._activation_checkboxes = []
        self._input_fields = []
        for index, parameter in enumerate(complementary_group._parameters):
            checkbox = Widgets.QCheckBox()
            input_field = from_type(parameter)

            checkbox.setToolTip(input_field._info)
            # noinspection PyUnresolvedReferences
            checkbox.stateChanged.connect(new_checkbox_trigger(index))
            # noinspection PyUnresolvedReferences
            input_field.text_modified.connect(new_member_modification_trigger(index))
            # noinspection PyUnresolvedReferences
            input_field.meta_modified.connect(new_member_modification_trigger(index))

            self._activation_checkboxes.append(checkbox)
            self._input_fields.append(input_field)

            h_layout = Widgets.QHBoxLayout()
            h_layout.addWidget(checkbox)
            h_layout.addWidget(input_field)
            v_layout.addLayout(h_layout)

        line = Widgets.QFrame(flags=QtCore.Qt.Widget)
        line.setFrameShape(Widgets.QFrame.HLine)
        line.setFrameShadow(Widgets.QFrame.Sunken)
        v_layout.addWidget(line)
        self.setLayout(v_layout)

    def as_adaptor_element(self):
        """
        This parameter type cannot be saved as a single element but requires a sub-configuration
        instead. See :method:`~ComplementaryGroupInput.as_config` instead.
        
        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError(
            'ComplementaryGroupInputs cannot be stored as single elements but require a '
            'sub-configuration instead'
        )

    # noinspection PyUnresolvedReferences
    def as_config(self, format_):
        """
        Obtain the parameter form as a sub-configuration.
         
        Parameters
        ----------
        format_ : unicode
            Must be either 'xml' or 'json'.
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
        active_input_fields = self._get_active_input_fields()
        if len(active_input_fields) != len(self._input_fields)-1:
            try:
                path = Adaptor.join_paths(self._group.path, self._group.name)
            except AttributeError:
                path = self._group.name
            raise InvalidInputError(
                '%s: Need specifications of exactly %d parameters (got %d instead)'
                % (path, len(self._input_fields)-1, len(active_input_fields)),
                self
            )
        texts, metas = self._get_active_texts_and_metas()
        for active_input_field in active_input_fields:
            name = active_input_field._parameter.name
            config.insert_element(
                name,
                config.Element(
                    name,
                    texts[name],
                    metas[name]
                )
            )
        return config

    def load_from_adaptor_element(self, element):
        """
        This parameter type cannot be loaded from a single element but requires a sub-configuration
        instead. See :method:`~ComplementaryGroupInput.load_from_source` instead.
        
        Raises
        ------
        NotImplementedError
            This method is not implemented. 
        """
        raise NotImplementedError(
            'ComplementaryGroupInputs cannot be loaded from a single elements but require a '
            'sub-configuration instead'
        )

    def load_from_source(self, config):
        """
        Fill the input forms with values from the given source.
         
        Parameters
        ----------
        config : :class:`ConfigurationAdaptor` derived class
        """
        # First deactivate all members in order to enter a fresh state.
        for checkbox in self._activation_checkboxes:
            checkbox.setChecked(False)

        for checkbox, input_field in zip(self._activation_checkboxes, self._input_fields):
            try:
                input_field.load_from_adaptor_element(
                    config.get_element(input_field._parameter.name)
                )
            except InvalidPathError:
                pass
            else:
                checkbox.setChecked(True)

    @property
    def needs_to_be_dumped(self):
        return True

    def _member_activation_changed(self, index, state):
        if state == 0:
            self._member_deactivated(index)
        else:
            self._member_activated(index)

    # noinspection PyUnresolvedReferences
    def _member_activated(self, index):
        number_of_active_members = len(list(filter(
            lambda x: x.isChecked(),
            self._activation_checkboxes
        )))
        number_of_members = len(self._activation_checkboxes)

        # If now N-1 members are active then disable the remaining one.
        if number_of_active_members == number_of_members - 1:
            remaining_member = list(filter(
                lambda x: not x.isChecked(),
                self._activation_checkboxes
            ))[0]
            corresponding_index = self._activation_checkboxes.index(remaining_member)
            self._input_fields[corresponding_index].setEnabled(False)
        # If now all members would be active deactivate the second to last one instead.
        elif number_of_active_members == number_of_members:
            self._activation_checkboxes[self._last_activated].setChecked(False)
            self._input_fields[self._last_activated].setEnabled(False)

        # Activate input field which corresponds to the checkbox.
        self._input_fields[index].setEnabled(True)
        self._last_activated = index

    # noinspection PyUnresolvedReferences
    def _member_deactivated(self, index):
        self._input_fields[index].setEnabled(False)

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    def _member_modified(self, index, *args):
        number_of_active_members = len(list(filter(
            lambda x: x.isChecked(),
            self._activation_checkboxes
        )))
        number_of_members = len(self._activation_checkboxes)

        # Special case: fewer than N-1 members are initially activated / selected. In that case
        # modifying an unselected member will auto-select it.
        if (not self._activation_checkboxes[index].isChecked()
                and number_of_active_members < number_of_members-1):
            self._activation_checkboxes[index].setChecked(True)
            self._last_activated = index
            number_of_active_members += 1

        # Update the remaining input field if exactly N-1 fields are active.
        if number_of_active_members == number_of_members-1:
            texts, metas = self._get_active_texts_and_metas()

            try:
                values = self._group.load_from_representation(texts, metas)
            except RepresentationError:
                return

            remaining_member = list(filter(
                lambda x: not x.isChecked(),
                self._activation_checkboxes
            ))[0]
            corresponding_index = self._activation_checkboxes.index(remaining_member)

            self._input_fields[corresponding_index].text =\
                six.text_type(values[corresponding_index])
            # In case the remaining parameter is a physical quantity we need to adjust the unit.
            self._input_fields[corresponding_index].meta = {
                'unit': getattr(self._input_fields[corresponding_index]._parameter, 'unit', None)
            }

    # noinspection PyUnresolvedReferences
    def _get_active_indices(self):
        return list(filter(
            lambda i: self._activation_checkboxes[i].isChecked(),
            range(len(self._activation_checkboxes))
        ))

    def _get_active_input_fields(self):
        return list(map(
            lambda i: self._input_fields[i],
            self._get_active_indices()
        ))

    # noinspection PyUnresolvedReferences
    def _get_active_texts_and_metas(self):
        active_indices = self._get_active_indices()
        texts = {
            self._input_fields[i]._parameter.name: self._input_fields[i].text
            for i in active_indices
        }
        metas = {
            self._input_fields[i]._parameter.name: self._input_fields[i].meta
            for i in active_indices
        }
        return texts, metas


class SubstitutionGroupInput(ParameterInput):
    PEER = parameters.SubstitutionParameterGroup

    def __init__(self, parameter_group, parent=None):
        super(SubstitutionGroupInput, self).__init__(parameter_group, parent)

        names = Widgets.QComboBox()
        self.input_fields = Widgets.QStackedWidget()
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

        h_layout = Widgets.QHBoxLayout()
        h_layout.addWidget(names)
        h_layout.addWidget(self.input_fields)
        self.setLayout(h_layout)

        self._set_info_button()

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

        self.vector = Widgets.QLineEdit()
        self.vector.setPlaceholderText('vector (separate elements with commas)')
        # noinspection PyUnresolvedReferences
        self.vector.textChanged.connect(self.text_modified.emit)

        layout = Widgets.QHBoxLayout()
        layout.addWidget(Widgets.QLabel(parameter.name))
        layout.addWidget(self.vector, 1)
        self.setLayout(layout)
        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        text_repr = six.text_type(self.vector.text()).strip()
        if not text_repr:
            return text_repr
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

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(VectorInput, self).setFocus()
        self.vector.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self.vector.setText(
                ', '.join(map(
                    six.text_type,
                    parameter.default
                ))
            )
        elif parameter.for_example is not None:
            self.vector.setText(
                ', '.join(map(
                    six.text_type,
                    parameter.for_example
                ))
            )


class DupletInput(VectorInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(DupletInput, self).__init__(parameter, parent)
        self.vector.setPlaceholderText('2-tuple (separate elements with commas)')


class TripletInput(VectorInput):
    PEER = None

    def __init__(self, parameter, parent=None):
        super(TripletInput, self).__init__(parameter, parent)
        self.vector.setPlaceholderText('3-tuple (separate elements with commas)')


class PhysicalVectorQuantityInput(ParameterInput):
    PEER = None

    meta_modified = QtCore.pyqtSignal(int)

    def __init__(self, parameter, parent=None):
        super(PhysicalVectorQuantityInput, self).__init__(parameter, parent)

        self.vector = Widgets.QLineEdit()
        self.vector.setPlaceholderText('vector (separate elements with commas)')
        # noinspection PyUnresolvedReferences
        self.vector.textChanged.connect(self.text_modified.emit)

        self.unit = PhysicalQuantityInput.setup_unit_field(parameter)
        # noinspection PyUnresolvedReferences
        self.unit.currentIndexChanged.connect(self.meta_modified.emit)

        h_layout = Widgets.QHBoxLayout()
        h_layout.addWidget(Widgets.QLabel(parameter.name))
        h_layout.addWidget(self.vector, 1)
        h_layout.addWidget(self.unit)
        self.setLayout(h_layout)

        self._set_default(parameter)
        self._set_info_button()

    @property
    def text(self):
        text_repr = six.text_type(self.vector.text()).strip()
        if not text_repr:
            return text_repr
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
        return {'unit': PhysicalQuantityInput.get_unit_from_field(self.unit)}

    @meta.setter
    def meta(self, value):
        PhysicalQuantityInput.set_unit_on_field(self.unit, value['unit'], self._parameter)

    # noinspection PyMethodOverriding,PyPep8Naming
    def setFocus(self):
        super(PhysicalVectorQuantityInput, self).setFocus()
        self.vector.setFocus()

    def _set_default(self, parameter):
        if parameter.is_expert:
            self.vector.setText(
                ', '.join(map(
                    six.text_type,
                    parameter.default
                ))
            )
            self.meta = {'unit': parameter.unit}
        elif parameter.for_example is not None:
            self.vector.setText(
                ', '.join(map(
                    six.text_type,
                    parameter.for_example
                ))
            )
            self.meta = {'unit': parameter.unit}


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
    parameter : :class:`Parameter`

    Returns
    -------
    input_field_cls : :class:`ParameterInput`
        The input field class corresponding to the given parameter's type.
    """
    potential_wrapper = parameter
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
            return PhysicalTripletInput(potential_wrapper)
        else:
            return TripletInput(potential_wrapper)
    elif issubclass(type(parameter), parameters._DupletParameterTemplate):
        if issubclass(parameter._element_type, parameters.PhysicalQuantityParameter):
            return PhysicalDupletInput(potential_wrapper)
        else:
            return DupletInput(potential_wrapper)
    elif issubclass(type(parameter), parameters._VectorParameterTemplate):
        if issubclass(parameter._element_type, parameters.PhysicalQuantityParameter):
            return PhysicalVectorQuantityInput(potential_wrapper)
        else:
            return VectorInput(potential_wrapper)

    try:
        # Needs to use type rather than isinstance because some parameter types subclass others.
        input_cls = list(filter(lambda x: type(parameter) == x.PEER, inputs))[0]
    except IndexError:
        raise TypeError('No input widget for parameter of type `%s`' % type(parameter))
    # noinspection PyCallingNonCallable
    return input_cls(potential_wrapper)
