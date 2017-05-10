"""Stream task module."""

from __future__ import absolute_import, division, print_function

from byte.core.models.task.base import Task
from byte.core.models.task.simple import SimpleTask, SimpleReadTask, SimpleSelectTask, SimpleWriteTask


class StreamTask(SimpleTask):
    """Base stream task class."""

    def __init__(self, executor):
        """Create stream task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(StreamTask, self).__init__(executor)

        self.stream = None

    @property
    def state(self):
        """Retrieve task state."""
        if self.stream is None:
            return Task.State.created

        if self.stream.closed:
            return Task.State.closed

        return Task.State.started

    def open(self):
        """Open task stream."""
        if self.closed:
            raise ValueError('Task has been closed')

        if self.started:
            raise ValueError('Task has already been started')

        # Open read stream
        self.stream = self.executor.read()

    def close(self):
        """Close task stream."""
        if self.closed:
            raise ValueError('Task has already been closed')

        if not self.started:
            return False

        # Close read stream
        if self.stream:
            self.stream.close()

        return True


class StreamReadTask(SimpleReadTask, StreamTask):
    """Base stream read task class."""

    pass


class StreamSelectTask(SimpleSelectTask, StreamTask):
    """Base stream select task."""

    pass


class StreamWriteTask(SimpleWriteTask, StreamTask):
    """Base stream write task."""

    pass
