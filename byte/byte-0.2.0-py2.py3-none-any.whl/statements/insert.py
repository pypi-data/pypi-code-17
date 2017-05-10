"""Insert statement module."""

from __future__ import absolute_import, division, print_function

from byte.statements.write import WriteStatement


class InsertStatement(WriteStatement):
    """Insert statement."""

    def __init__(self, collection, model, items=None, properties=None, query=None, state=None):
        """Create insert statement.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param items: Items to insert
        :type items: list or None

        :param properties: Insertion properties (?)
        :type properties: tuple or None

        :param query: Insertion query
        :type query: object

        :param state: Initial state
        :type state: dict or None
        """
        super(InsertStatement, self).__init__(collection, model, state=state)

        self.items = items
        self.properties = properties
        self.query = query

    def upsert(self):
        """Update item, or insert if it doesn't exist."""
        raise NotImplementedError
