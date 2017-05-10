"""Memory executor module."""

from __future__ import absolute_import, division, print_function

from byte.compilers.core.models import InsertOperation, SelectOperation
from byte.executors.core.base import SimpleExecutorPlugin
from byte.executors.memory.revision import MemoryRevision
from byte.executors.memory.tasks import MemorySelectTask, MemoryWriteTask


class MemoryExecutor(SimpleExecutorPlugin):
    """Memory executor class."""

    key = 'memory'

    class Meta(SimpleExecutorPlugin.Meta):
        """Memory executor metadata."""

        scheme = 'memory'

    def __init__(self, collection, model):
        """Create memory executor.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model
        """
        super(MemoryExecutor, self).__init__(collection, model)

        self.items = {}

    def execute(self, statement):
        """Execute statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement
        """
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        if isinstance(operation, InsertOperation):
            return MemoryWriteTask(self, [operation]).execute()

        if isinstance(operation, SelectOperation):
            return MemorySelectTask(self, operation).execute()

        raise NotImplementedError

    def revision(self):
        """Create revision."""
        return MemoryRevision(self)

    def update(self, *args, **kwargs):
        """Update items."""
        self.items.update(*args, **kwargs)
