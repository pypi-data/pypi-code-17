"""Executor revision model module."""

from __future__ import absolute_import, division, print_function


class Revision(object):
    """Base executor revision class."""

    def __init__(self, executor):
        """Create executor revision.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        self.executor = executor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
