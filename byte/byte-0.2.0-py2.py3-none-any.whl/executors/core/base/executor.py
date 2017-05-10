"""Executor base module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Executor(object):
    """Base executor class."""

    def __init__(self, collection, model):
        """Create executor.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model
        """
        self.collection = collection
        self.model = model

        self._compiler = None

    @property
    def compiler(self):
        """Retrieve current compiler."""
        if not self._compiler:
            self._compiler = self.construct_compiler()

        return self._compiler

    @property
    def plugins(self):
        """Retrieve plugins manager."""
        if not self.collection:
            return None

        return self.collection.plugins

    def close(self):
        """Close executor."""
        raise NotImplementedError

    def execute(self, statement):
        """Execute statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement
        """
        raise NotImplementedError

    def construct_compiler(self):
        """Construct compiler."""
        return self.plugins.get_compiler('operation')(self)


class ExecutorPlugin(Executor, Plugin):
    """Base executor plugin class."""

    key = None
    priority = Plugin.Priority.Medium

    class Meta(Plugin.Meta):
        """Executor plugin metadata."""

        kind = 'executor'

        content_type = None
        extension = None
        scheme = None

        @classmethod
        def transform(cls):
            """Transform executor metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.scheme = resolve_tuples(
                cls.scheme,
                lambda value: (Plugin.Priority.Medium, value)
            )

        @classmethod
        def validate(cls, executor):
            """Validate executor metadata.

            :param executor: Executor
            :type executor: ExecutorPlugin
            """
            assert executor.key, (
                'Plugin has no "key" attribute defined'
            )

            assert isinstance(executor.key, string_types), (
                'Invalid value provided for the plugin "key" attribute (expected str)'
            )

            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )

            assert is_list_of(cls.scheme, (int, string_types)), (
                'Invalid value provided for the "scheme" attribute (expected str, [str], [(int, str)])'
            )

            assert len(cls.scheme) > 0, (
                'Invalid value provided for the "scheme" attribute (at least one scheme is required)'
            )
