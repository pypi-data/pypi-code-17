"""Memory executor task module."""

from __future__ import absolute_import, division, print_function

from byte.core.models import Task, SimpleTask, SimpleReadTask, SimpleSelectTask, SimpleWriteTask

import six


class MemoryTask(SimpleTask):
    """Memory task."""

    def __init__(self, executor):
        """Create memory task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(MemoryTask, self).__init__(executor)

        self._state = Task.State.created

    @property
    def state(self):
        """Retrieve task state."""
        return self._state

    def open(self):
        """Open task."""
        # Update state
        self._state = Task.State.started

    def close(self):
        """Close task."""
        # Update state
        self._state = Task.State.closed

        return True


class MemoryReadTask(SimpleReadTask, MemoryTask):
    """Memory read task."""

    pass


class MemorySelectTask(SimpleSelectTask, MemoryReadTask):
    """Memory select task."""

    def decode(self):
        """Decode items."""
        return six.itervalues(self.executor.items)


class MemoryWriteTask(SimpleWriteTask, MemoryTask):
    """Memory write task."""

    def decode(self):
        """Decode items."""
        return six.itervalues(self.executor.items)

    def encode(self, revision, items):
        """Encode items.

        :param revision: Revision
        :type revision: byte.executors.memory.revision.MemoryRevision

        :param items: Items
        :type items: dict
        """
        revision.items.update(items)
