"""Simple executor base module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base.executor import Executor, ExecutorPlugin


class SimpleExecutor(Executor):
    """Base simple executor class."""

    def revision(self):
        """Create revision."""
        raise NotImplementedError


class SimpleExecutorPlugin(SimpleExecutor, ExecutorPlugin):
    """Base simple executor plugin class."""

    pass
