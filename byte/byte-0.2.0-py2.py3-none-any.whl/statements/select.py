"""Select statement module."""

from __future__ import absolute_import, division, print_function

from byte.statements.core.base import operation
from byte.statements.where import WhereStatement

from six import string_types


class SelectStatement(WhereStatement):
    """Select statement."""

    def __init__(self, collection, model, properties=None, state=None):
        """Create select statement.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param properties: Properties to retrieve (or :code:`None` to retrieve all properties)
        :type properties: tuple or None

        :param state: Initial state
        :type state: dict or None
        """
        super(SelectStatement, self).__init__(collection, model, state=state)

        self.properties = properties

    def count(self):
        """Execute statement, and retrieve an integer representing the number of objects in the result."""
        return len(self.execute())

    def exists(self):
        """Execute statement, and retrieve boolean indicating if any results were returned."""
        raise NotImplementedError

    def group_by(self, *args, **kwargs):
        """Group results by properties."""
        raise NotImplementedError

    def iterator(self):
        """Execute statement, and retrieve the item iterator."""
        return iter(self.execute())

    def last(self):
        """Execute statement, and retrieve the last item from the results."""
        raise NotImplementedError

    @operation
    def limit(self, count):
        """Set query limit."""
        self.state['limit'] = count

    @operation
    def offset(self, count):
        """Set query offset."""
        self.state['offset'] = count

    @operation
    def order_by(self, *properties):
        """Order results by :code:`properties`."""
        if 'order_by' not in self.state:
            self.state['order_by'] = []

        for prop in properties:
            prop, order, options = self._parse_property_tuple(prop)

            # Resolve `order` value
            if order:
                order = order.lower()

                if order.startswith('asc'):
                    order = 'ascending'
                elif order.startswith('desc'):
                    order = 'descending'

            # Build options dictionary
            if not options:
                options = {
                    'order': order or 'ascending'
                }

            # Resolve property key
            if isinstance(prop, string_types):
                prop = self.model.Internal.properties_by_key[prop]

            # Append property definition to state
            self.state['order_by'].append((prop, options))

    @staticmethod
    def _parse_property_tuple(prop):
        options = None
        order = None

        if type(prop) is not tuple:
            return prop, order, options

        if len(prop) != 2:
            raise ValueError('Invalid property definition')

        if type(prop[1]) is not dict and not isinstance(prop[1], string_types):
            raise ValueError('Invalid property definition')

        if isinstance(prop[1], string_types):
            prop, order = prop
        else:
            prop, options = prop

        return prop, order, options

    def __iter__(self):
        """Execute statement, and retrieve the item iterator."""
        return self.iterator()

    def __len__(self):
        """Execute statement, and retrieve an integer representing the number of objects in the result."""
        return self.count()
