"""Collection format base module."""

from __future__ import absolute_import, division, print_function

from byte.compilers.core.models import DeleteOperation, InsertOperation, SelectOperation, UpdateOperation
from byte.formats.core.base.format import Format, FormatPlugin

__all__ = (
    'CollectionFormat',
    'CollectionFormatPlugin'
)


class CollectionFormat(Format):
    """Collection format base class."""

    def execute(self, executor, operation):
        """Execute operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Operation
        :type operation: byte.compilers.core.models.Operation
        """
        if isinstance(operation, DeleteOperation):
            return self.delete(executor, operation)

        if isinstance(operation, InsertOperation):
            return self.insert(executor, operation)

        if isinstance(operation, SelectOperation):
            return self.select(executor, operation)

        if isinstance(operation, UpdateOperation):
            return self.update(executor, operation)

        raise NotImplementedError('Unsupported operation: %s' % (operation,))

    def delete(self, executor, operation):
        """Execute delete operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Delete operation
        :type operation: byte.compilers.core.models.DeleteOperation
        """
        raise NotImplementedError('Delete operation hasn\'t been implemented')

    def insert(self, executor, operation):
        """Execute insert operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Insert operation
        :type operation: byte.compilers.core.models.InsertOperation
        """
        raise NotImplementedError('Insert operation hasn\'t been implemented')

    def select(self, executor, operation):
        """Execute select operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Select operation
        :type operation: byte.compilers.core.models.SelectOperation
        """
        raise NotImplementedError('Select operation hasn\'t been implemented')

    def update(self, executor, operation):
        """Execute update operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Update operation
        :type operation: byte.compilers.core.models.UpdateOperation
        """
        raise NotImplementedError('Update operation hasn\'t been implemented')


class CollectionFormatPlugin(CollectionFormat, FormatPlugin):
    """Collection format plugin class."""

    format_type = 'collection'
