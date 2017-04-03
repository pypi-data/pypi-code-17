# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os.path

# noinspection PyPackageRequirements,PyUnresolvedReferences
from PyQt4 import QtGui

from anna.dependencies import Dependency
from anna.frontends.qt.forms import ParameterForm


class ComponentView(QtGui.QWidget):
    """
    QWidget containing the basic information (title, doc string) about a component
    *without* its parameters.
    """
    def __init__(self, component, title=None, parent=None):
        """
        Initialize the widget with a component.

        Parameters
        ----------
        component
            The component to be displayed
        title : unicode, optional
            An optional string to be displayed instead of the component's name
        parent : QWidget, optional
        """
        super(ComponentView, self).__init__(parent=parent)

        if not isinstance(component, type):
            raise TypeError('Requires a class as component (got %s instead)' % component)
        self._component = component

        info_button = QtGui.QPushButton(
            QtGui.QIcon(os.path.join(os.path.split(__file__)[0], 'icons/info.png')), ''
        )
        info_button.setFixedHeight(30)
        info_button.setFixedWidth(30)

        def show_info():
            if component.__doc__ is None:
                text = 'Component %s does not provide any information.' % component.__name__
            else:
                text = component.__doc__
            QtGui.QMessageBox.information(
                self,
                component.__name__,
                text
            )

        # noinspection PyUnresolvedReferences
        info_button.clicked.connect(show_info)

        layout = QtGui.QVBoxLayout()
        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(QtGui.QLabel('<b>%s</b>' % (title or component.__name__)))
        h_layout.addStretch(1)
        h_layout.addWidget(info_button)
        layout.addLayout(h_layout)

        if component.__doc__ is not None:
            doc_brief = component.__doc__.split('\n\n')[0].strip()
            doc_brief_widget = QtGui.QTextEdit()
            doc_brief_widget.setText(doc_brief)
            doc_brief_widget.setReadOnly(True)
            layout.addWidget(doc_brief_widget)

        self.setLayout(layout)


class ParametrizedComponentView(ComponentView):
    """
    QWidget containing input forms for all parameters of a component as well as for
    all dependency components.
    """
    def __init__(self, component, title=None, parent=None):
        """
        Initialize the widget with a component.

        Parameters
        ----------
        component
            The (parametrized) component to be displayed
        title : unicode, optional
            An optional string to be displayed instead of the component's name
        parent : QWidget, optional
        """
        super(ParametrizedComponentView, self).__init__(component, title, parent)

        self._parameter_form = ParameterForm(component.get_parameters())
        self.layout().addWidget(self._parameter_form)

        self._dependency_views = []
        dependencies = self._get_dependencies()
        if dependencies:
            self.layout().addWidget(QtGui.QLabel('<u><b>Dependencies</b></u>'))
        for dependency in dependencies:
            self._dependency_views.append(ParametrizedComponentView(dependency.cls))
            self.layout().addWidget(self._dependency_views[-1])

    def dump_as_xml(self):
        return self.dump_as('xml')

    def dump_as_json(self):
        return self.dump_as('json')

    def dump_as(self, format_):
        if format_ not in ('json', 'xml'):
            raise ValueError(
                'format_ must be either "xml" or "json" (got "%s" instead)'
                % format_
            )
        config = self._parameter_form.dump_as(format_)
        for dependency in self._dependency_views:
            config.insert_config(self._component.CONFIG_PATH, dependency.dump_as(format_))
        return config

    def load_from_source(self, configuration):
        self._parameter_form.load_from_source(configuration)

    def _get_dependencies(self):
        return filter(
            lambda x: isinstance(x, Dependency),
            map(
                lambda x: getattr(self._component, x),
                dir(self._component)
            )
        )
