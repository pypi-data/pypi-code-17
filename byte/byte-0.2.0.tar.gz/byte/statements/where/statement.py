"""Where statement module."""

from __future__ import absolute_import, division, print_function

from byte.expressions import (
    And, BaseExpression, Equal, GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual,
    NotEqual, Or
)
from byte.statements.core.base import Statement, operation
from byte.statements.where.parser import WHERE

from six import string_types


class WhereStatement(Statement):
    """Where statement."""

    @operation
    def where(self, *args):
        """Retrieve items matching expressions (args)."""
        if not args:
            return

        if 'where' not in self.state:
            self.state['where'] = []

        # Parse string, and append expressions to state
        if isinstance(args[0], string_types):
            self.state['where'].extend(self.__parse_string(*args))
            return

        # Append expressions to state
        for value in args:
            if isinstance(value, BaseExpression):
                self.state['where'].append(value)
            else:
                if len(args) > 1:
                    raise ValueError('Only one primary key expression allowed')

                self.state['where'].append(Equal(self.model.Internal.primary_key, value))

    def __parse_string(self, value, *parameters):
        if not value:
            return []

        if len(parameters) == 1 and type(parameters[0]) is tuple:
            parameters = parameters[0]

        # Parse expressions from string
        offset, expression = self.__parse_string_parts(
            WHERE.parseString(value).asList(),
            parameters=parameters
        )

        if (offset or parameters) and offset != len(parameters):
            raise Exception('Found %d parameter token(s), but only %d value(s) were provided' % (
                offset, len(parameters)
            ))

        if isinstance(expression, And):
            return expression.values

        return [expression]

    def __parse_string_parts(self, parts, offset=0, parameters=None):
        if (len(parts) - 1) % 2 > 0:
            raise ValueError('Incorrect number of expression parts')

        if parts[0] == '(' and parts[-1] == ')':
            parts = parts[1:-1]

        expressions = []
        pos = 0

        while pos < len(parts):
            # Retrieve left value
            if expressions:
                left = expressions[-1]
            else:
                left = parts[pos]
                pos += 1

            # Retrieve operator and right value
            op = parts[pos]
            right = parts[pos + 1]
            pos += 2

            # Resolve values
            offset, left = self.__resolve_string_value(
                left,
                offset=offset,
                parameters=parameters
            )

            offset, right = self.__resolve_string_value(
                right,
                offset=offset,
                parameters=parameters
            )

            # Append expression
            expression = self.__construct_expression(expressions, op, left, right)

            if expression:
                expressions.append(expression)

        if len(expressions) == 1:
            return offset, expressions[0]

        return offset, And(*expressions)

    def __resolve_string_value(self, value, offset=0, parameters=None):
        if isinstance(value, BaseExpression):
            return offset, value

        if isinstance(value, list):
            return self.__parse_string_parts(
                value,
                offset=offset,
                parameters=parameters
            )

        # String
        if value == '?':
            if offset < len(parameters):
                return offset + 1, parameters[offset]

            return offset + 1, '?'

        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            return offset, value[1:-1]

        # Integer
        try:
            return offset, int(value)
        except (TypeError, ValueError):
            pass

        # Column
        return offset, self.model.Internal.properties_by_name[value]

    def __construct_expression(self, expressions, op, left, right):
        if op in ['eq', '=', '==']:
            return Equal(left, right)

        if op in ['ne', '!=']:
            return NotEqual(left, right)

        if op in ['lt', '<']:
            return LessThan(left, right)

        if op in ['le', '<=']:
            return LessThanOrEqual(left, right)

        if op in ['gt', '>']:
            return GreaterThan(left, right)

        if op in ['ge', '>=']:
            return GreaterThanOrEqual(left, right)

        if op == 'and':
            if not expressions:
                expressions.append(left)

            expressions.append(right)
            return None

        if op == 'or':
            return Or(left, right)

        raise NotImplementedError
