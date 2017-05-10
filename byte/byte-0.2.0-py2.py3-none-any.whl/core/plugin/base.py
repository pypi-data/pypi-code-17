"""Plugin base module."""

from __future__ import absolute_import, division, print_function


class Plugin(object):
    """Base plugin class."""

    class Meta(object):
        """Plugin metadata."""

        kind = None

        @classmethod
        def transform(cls):
            """Transform metadata."""
            pass

        @classmethod
        def validate(cls, plugin):
            """Validate metadata.

            :param plugin: Plugin
            :type plugin: Plugin
            """
            return True

    class Priority(object):
        """Plugin priorities."""

        Low     =  1000  # noqa
        Medium  =     0  # noqa
        High    = -1000  # noqa
