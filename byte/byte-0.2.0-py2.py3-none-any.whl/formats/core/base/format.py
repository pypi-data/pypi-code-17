"""Format base module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.resolve import resolve_tuples
from byte.core.helpers.validate import is_list_of
from byte.core.plugin.base import Plugin

from six import string_types

__all__ = (
    'Format',
    'FormatPlugin'
)


class Format(object):
    """Format base class."""

    pass


class FormatPlugin(Format, Plugin):
    """Format plugin class."""

    key = None
    priority = Plugin.Priority.Medium

    class Meta(Plugin.Meta):
        """Format metadata."""

        kind = 'format'
        format_type = None

        content_type = None
        extension = None

        @classmethod
        def transform(cls):
            """Transform format metadata."""
            cls.extension = resolve_tuples(
                cls.extension,
                lambda value: (Plugin.Priority.Medium, value)
            )

            cls.content_type = resolve_tuples(
                cls.content_type,
                lambda value: (Plugin.Priority.Medium, value)
            )

        @classmethod
        def validate(cls, fmt):
            """Validate format metadata.

            :param fmt: Format
            :type fmt: FormatPlugin
            """
            assert fmt.key, (
                'Plugin has no "key" attribute defined'
            )

            assert isinstance(fmt.key, string_types), (
                'Invalid value provided for the plugin "key" attribute (expected str)'
            )

            assert cls.extension is None or is_list_of(cls.extension, (int, string_types)), (
                'Invalid value provided for the "extension" attribute (expected str, [str], [(int, str)])'
            )

            assert cls.content_type is None or is_list_of(cls.content_type, (int, string_types)), (
                'Invalid value provided for the "content_type" attribute (expected str, [str], [(int, str)])'
            )
