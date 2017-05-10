"""Simple task module."""

from __future__ import absolute_import, division, print_function

from byte.compilers.core.models import InsertOperation
from byte.core.models.task.base import Task, ReadTask, SelectTask, WriteTask


class SimpleTask(Task):
    """Base simple task class."""

    pass


class SimpleReadTask(ReadTask, SimpleTask):
    """Base simple read task class."""

    pass


class SimpleSelectTask(SelectTask, SimpleTask):
    """Base simple select task."""

    def decode(self):
        """Decode items."""
        raise NotImplementedError

    def execute(self):
        """Execute task."""
        self.open()

        return self

    def items(self):
        """Retrieve items from task."""
        if self.closed:
            raise ValueError('Task has been closed')

        if not self.started:
            raise ValueError('Task hasn\'t been started')

        for value in self.decode():
            item = self.model.from_plain(
                value,
                translate=True
            )

            if not self.is_match(item, self.operation.where):
                continue

            yield item

    @staticmethod
    def is_match(item, expressions):
        """Check if item matches expressions.

        :param item: Item
        :type item: byte.model.Model

        :param expressions: Expressions
        :type expressions: list of byte.base.BaseExpression
        """
        for expression in expressions:
            if not expression.execute(item):
                return False

        return True


class SimpleWriteTask(WriteTask, SimpleTask):
    """Base simple write task class."""

    def decode(self):
        """Decode items."""
        raise NotImplementedError

    def encode(self, revision, items):
        """Encode items."""
        raise NotImplementedError

    def execute(self):
        """Execute task."""
        self.open()

        # Retrieve primary key for model
        primary_key = self.model.Internal.primary_key

        if not primary_key:
            raise Exception('Missing required primary key')

        # Create revision
        with self.executor.revision() as revision:
            # Encode items, and write to revision stream
            self.encode(revision, self.run(primary_key))

            # Close task
            self.close()

        return self

    def run(self, primary_key):
        """Run insertion operation."""
        # Retrieve insertion operations
        insertions = self.index_insertions(primary_key)

        # Decode items from collection
        for value in self.decode():
            # Parse item
            item = self.model.from_plain(
                value,
                translate=True
            )

            # Retrieve primary key for item
            pk = primary_key.get(item)

            if pk in insertions:
                raise Exception('Item with key %r already exists' % (pk,))

            # TODO Run item operations (e.g. delete, update)

            # Emit item
            yield (pk, item.to_plain())

        # Emit insertions
        for pk, item in insertions.items():
            yield (pk, item)

    def index_insertions(self, primary_key):
        """Index insertion operations by primary key."""
        insertions = {}

        for operation in self.operations:
            if not isinstance(operation, InsertOperation):
                continue

            for item in operation.items:
                key = primary_key.get(item)

                if key is None:
                    # TODO Support automatic primary keys for items (e.g. auto increment)
                    raise Exception('No primary key defined for item: %s' % (item,))

                if key in insertions:
                    raise Exception('Multiple insertions found for item with key %r' % (key,))

                insertions[key] = item

        return insertions
