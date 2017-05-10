"""byte - expressions module."""

from __future__ import absolute_import, division, print_function

from byte.base import BaseExpression, BaseProperty


def get_value(item, operand):
    """Retrieve property value.

    :param item: Item
    :type item: byte.model.Model

    :param operand: Operand
    :type operand: any
    """
    if isinstance(operand, BaseProperty):
        return operand.get(item)

    return operand


def resolve_value(value):
    """Resolve expression value.

    :param value: Value
    :type value: any
    """
    if isinstance(value, Expression):
        return value.value

    return value


class Expression(BaseExpression):
    """Simple expression."""

    def __init__(self, value):
        """Create simple expression.

        :param value: Value
        """
        self.value = resolve_value(value)

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.value == other.value
        )

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)


class CompoundExpression(BaseExpression):
    """Base compound-expression."""

    def __init__(self, left, right):
        """Create compound-expression.

        :param left: Left value
        :param right: Right value
        """
        self.left = resolve_value(left)
        self.right = resolve_value(right)

    def matches(self, left, right):
        """Check if values match.

        :param left: Left value
        :param right: Right value
        """
        raise NotImplementedError

    def execute(self, item):
        """Check if item matches expression.

        :param item: Item
        :type item: byte.model.Model
        """
        return self.matches(
            get_value(item, self.left),
            get_value(item, self.right)
        )

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.left == other.left and
            self.right == other.right
        )

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)


class MultiExpression(BaseExpression):
    """Base multi-expression."""

    def __init__(self, *values):
        """Create multi-expression.

        :param values: Values
        """
        self.values = [resolve_value(value) for value in values]

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.values == other.values
        )

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([
            repr(value)
            for value in self.values
        ]))


class IsNull(Expression):
    """Is-Null expression."""

    def execute(self, item):
        """Check if item matches expression.

        :param item: Item
        :type item: byte.model.Model
        """
        return get_value(item, self.value) is None


class In(Expression):
    """In expression."""

    def __init__(self, prop, items):
        """Create in expression.

        :param prop: Property
        :type prop: byte.property.Property

        :param items: Items
        """
        super(In, self).__init__(prop)

        self.items = items

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.prop == other.prop and
            self.items == other.items
        )

    def __repr__(self):
        return 'In(%r, %r)' % (self.prop, self.items)


class And(MultiExpression):
    """And expression."""

    pass


class Or(MultiExpression):
    """Or expression."""

    pass


class Equal(CompoundExpression):
    """Equal expression."""

    def matches(self, left, right):
        """Check if values match.

        :param left: Left value
        :param right: Right value
        """
        return left == right


class NotEqual(CompoundExpression):
    """Not-Equal expression."""

    pass


class LessThan(CompoundExpression):
    """Less-Than expression."""

    pass


class LessThanOrEqual(CompoundExpression):
    """Less-Than-Or-Equal expression."""

    pass


class GreaterThan(CompoundExpression):
    """Greater-Than expression."""

    pass


class GreaterThanOrEqual(CompoundExpression):
    """Greater-Than-Or-Equal expression."""

    pass
