"""Update statement module."""

from __future__ import absolute_import, division, print_function

from byte.statements.where import WhereStatement
from byte.statements.write import WriteStatement


class UpdateStatement(WhereStatement, WriteStatement):
    """Update statement."""

    def __init__(self, collection, model, data=None, state=None):
        """Create update statement.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param data: Data
        :type data: dict or None

        :param state: Initial state
        :type state: dict or None
        """
        super(UpdateStatement, self).__init__(collection, model, state=state)

        self.data = data
