import os

import re
import yaml

from codeskeleton import exceptions
from codeskeleton import template
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject
from codeskeleton.spec.variables import Variables


class AbstractToplevel(AbstractSpecObject):
    """
    Abstract base class for parsers/data structures for an entire spec file.
    """
    @classmethod
    def from_file(cls, yaml_file_path):
        base_directory = os.path.dirname(yaml_file_path)
        with open(yaml_file_path, encoding='utf-8') as f:
            data = yaml.load(f.read())
        toplevel = cls(base_directory=base_directory)
        toplevel.deserialize(data)
        return toplevel

    def __init__(self, base_directory, id=None, title=None, description=None, context=None, variables=None):
        """

        Args:
            base_directory: Base directory where the files for the spec template files are located.
                Normally the directory where the spec file is located.
            context (optional): The context this spec belongs to. Typically the programming
                language (python, javascript, ...), or the framework (django, react, ...) or
                a project name for a project specific spec. Must be a single word, all in
                lowercase (can only contain a-z and numbers).
            id: The ID of the spec. Used to uniquely identify the spec within the ``context``.
            title (optional): Short user friendly description of what the spec creates.
            description (optional): Long user friendly description of what the spec creates.
            variables (codeskeleton.spec.variables.Variables): Variable definitions for the spec.
        """
        self.base_directory = base_directory
        self.id = id
        self.title = title
        self.description = description
        self.context = context
        self.variables = variables or Variables()

    @property
    def full_id(self):
        return '{}.{}'.format(self.context, self.id)

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A dict like object with one of the following key/value pairs:

                - ``id``: See :meth:`.__init__`.
                - ``title`` (optional): See :meth:`.__init__`.
                - ``description`` (optional): See :meth:`.__init__`.
                - ``context`` (optional): See :meth:`.__init__`.
                - ``variables`` (optional): Data on a format that can be parsed by
                  :meth:`codeskeleton.spec.variables.Variables.deserialize`.
        """
        self.id = data.get('id', None)
        self.title = data.get('title', None)
        self.description = data.get('description', None)
        self.context = data.get('context', None)
        self.variables = Variables()
        self.variables.deserialize(data.get('variables', {}))

    def make_template_environment(self):
        """
        Make a jinja2 template environment for this tree.

        See :func:`codeskeleton.template.make_environment`.
        """
        return template.make_environment(base_directory=self.base_directory,
                                         variables=self.variables.values_as_dict())

    def validate_spec(self):
        if not self.id:
            raise exceptions.SpecValidationError(
                path='id',
                message='This attribute is required.')
        if not self.context:
            raise exceptions.SpecValidationError(
                path='context',
                message='This attribute is required.')
        if not re.match(r'^[a-z0-9]+$', self.context):
            raise exceptions.SpecValidationError(
                path='context',
                message='Must be a lowercase single word containing only a-z and numbers.')
        self.variables.validate_spec(path='variables')
