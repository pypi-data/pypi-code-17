from typing import Any
from operator import not_
from functools import reduce

__all__ = [
    'complement', 'compose', 'dec', 'even', 'identity', 'inc', 'odd'
]


sentinel = object()


def identity(x: Any) -> Any:
    """
    Returns the same values passed as arguments

    >>> x = (10, 20)
    >>> identity(x)
    (10, 20)
    """
    return x


def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def complement(func):
    return compose(not_, func)


def inc(x: int) -> int:
    """
    Increments argument by 1

    >>> inc(10)
    11
    """
    return x + 1


def dec(x: int) -> int:
    """
    Decrements argument by 1

    >>> dec(5)
    4
    """
    return x - 1


def even(x: int) -> bool:
    """
    Returns True if something
    >>> even(2)
    True
    """
    return x % 2 == 0


def odd(x: int) -> bool:
    """
    >>> even(3)
    False
    """
    return x % 2 == 1
