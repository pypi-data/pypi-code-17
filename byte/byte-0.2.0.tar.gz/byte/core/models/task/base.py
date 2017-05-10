"""Task base module."""

from __future__ import absolute_import, division, print_function

__all__ = (
    'Task',
    'ReadTask',
    'WriteTask'
)


class Task(object):
    """Base task class."""

    class State(object):
        """Task states."""

        created = 0
        started = 1
        closed  = 2  # noqa

    def __init__(self, executor):
        """Create task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        self.executor = executor

    @property
    def closed(self):
        """Retrieve boolean representing the task closed state."""
        return self.state == Task.State.closed

    @property
    def collection(self):
        """Retrieve collection."""
        return self.executor.collection

    @property
    def model(self):
        """Retrieve model."""
        return self.executor.model

    @property
    def started(self):
        """Retrieve boolean representing the task started state."""
        return self.state == Task.State.started

    @property
    def state(self):
        """Retrieve task state."""
        raise NotImplementedError

    def open(self):
        """Open task."""
        raise NotImplementedError

    def execute(self):
        """Execute task."""
        raise NotImplementedError

    def close(self):
        """Close task."""
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ReadTask(Task):
    """Base read task class."""

    def __init__(self, executor, operation):
        """Create read task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Operation
        :type operation: byte.compilers.core.models.Operation
        """
        super(ReadTask, self).__init__(executor)

        self.operation = operation


class SelectTask(ReadTask):
    """Base select task class."""

    def items(self):
        """Retrieve items from task."""
        raise NotImplementedError

    def __iter__(self):
        return iter(self.items())


class WriteTask(Task):
    """Base write task class."""

    def __init__(self, executor, operations):
        """Create read task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operations: Operations
        :type operations: list of byte.compilers.core.models.Operation
        """
        super(WriteTask, self).__init__(executor)

        self.operations = operations
