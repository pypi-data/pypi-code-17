"""Base compiler module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types


class Compiler(object):
    """Base compiler class."""

    def __init__(self, executor):
        """Create compiler.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        self.executor = executor

    @property
    def collection(self):
        """Retrieve collection.

        :return: Collection
        :rtype: byte.collection.Collection
        """
        if not self.executor:
            return None

        return self.executor.collection

    @property
    def model(self):
        """Retrieve model.

        :return: Model
        :rtype: byte.model.Model
        """
        if not self.executor:
            return None

        return self.executor.model

    def compile(self, statement):
        """Compile statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement
        """
        raise NotImplementedError


class CompilerPlugin(Compiler, Plugin):
    """Base compiler plugin class."""

    key = None
    priority = Plugin.Priority.Medium

    class Meta(Plugin.Meta):
        """Compiler metadata."""

        kind = 'compiler'

        content_type = None
        extension = None

        @classmethod
        def transform(cls):
            """Transform compiler metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Medium, value)
            )

        @classmethod
        def validate(cls, compiler):
            """Validate compiler metadata.

            :param compiler: Compiler
            :type compiler: Compiler
            """
            assert compiler.key, (
                'Plugin has no "key" attribute defined'
            )

            assert isinstance(compiler.key, string_types), (
                'Invalid value provided for the plugin "key" attribute (expected str)'
            )

            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )
