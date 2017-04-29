from typing import Any as _Any

class Expect(object):
    def __init__(self, value: _Any):
        self.value = value
        self.negate = False
        self.negate_term = ""

    @property
    def does(self):
        return self

    @property
    def to(self):
        return self

    @property
    def be(self):
        return self

    def _not(self):
        self.negate = True
        self.negate_term = "not"
        return self

    @property
    def isnt(self):
        self._not()
        self.negate_term = "isn't"
        return self

    @property
    def doesnt(self):
        self._not()
        self.negate_term = "doesn't"
        return self

    def equal(self, test):
        from expectlib.comparison import Equal
        return Equal(self.value, test, self.negate, self.negate_term)

    def greater_than(self, test):
        from expectlib.comparison import GreaterThan
        return GreaterThan(self.value, test, self.negate, self.negate_term)

    def lesser_than(self, test):
        from expectlib.comparison import LesserThan
        return LesserThan(self.value, test, self.negate, self.negate_term)

    def greater_than_or_equal(self, test):
        from expectlib.comparison import GreaterThanOrEqual
        return GreaterThanOrEqual(self.value, test, self.negate, self.negate_term)

    def lesser_than_or_equal(self, test):
        from expectlib.comparison import LesserThanOrEqual
        return LesserThanOrEqual(self.value, test, self.negate, self.negate_term)

    def is_equal(self, test):
        from expectlib.comparison import Is
        return Is(self.value, test, self.negate, self.negate_term)

    def true(self):
        return self.is_equal(True)

    def false(self):
        return self.is_equal(False)

    def none(self):
        return self.is_equal(None)

    def contain(self, test):
        from expectlib.comparison import Contain
        return Contain(self.value, test, self.negate, self.negate_term)

    def have(self, test):
        return self.contain(test)

    def match(self, test):
        from expectlib.comparison import Match
        return Match(self.value, test, self.negate, self.negate_term)

    def start_with(self, test):
        from expectlib.comparison import StartWith
        return StartWith(self.value, test, self.negate, self.negate_term)

    def end_with(self, test):
        from expectlib.comparison import EndWith
        return EndWith(self.value, test, self.negate, self.negate_term)

    def empty(self):
        from expectlib.comparison import Empty
        return Empty(self.value, None, self.negate, self.negate_term)

    def __call__(self, *args, **kwargs):
        return self

    def __eq__(self, other):
        return self.equal(other)

    def __lt__(self, other):
        return self.lesser_than(other)

    def __gt__(self, other):
        return self.greater_than(other)

    def __le__(self, other):
        return self.lesser_than_or_equal(other)

    def __ge__(self, other):
        return self.greater_than_or_equal(other)

    def __floordiv__(self, other):
        return self.match(other)

    def __lshift__(self, other):
        return self.start_with(other)

    def __rshift__(self, other):
        return self.end_with(other)

    def __xor__(self, other):
        return self.contain(other)

    def __mod__(self, other):
        return self.is_equal(other)

    def __invert__(self):
        self._not()
        return self


def expect(value: _Any):
    return Expect(value)
