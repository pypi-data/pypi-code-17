#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import TypeVar, Iterator, Iterable, Callable

T = TypeVar('T')

def fjoin(functions: Iterable[Callable[[T], T]]) -> Callable:
    """fjoin([f1, f2, ..., fn])(x) = fn(...f2(f1(x))) (not f1(f2(...fn(x))))

    >>> fjoin([])(1)
    1
    >>> fjoin([lambda x: x])(0)
    0
    >>> fjoin([lambda x: x + 1, lambda x: 2*x, lambda x: x**2])(3)
    64
    """
    def _joined(arg: T):
        res = arg
        for f in functions:
            res = f(res)
        return res
    return _joined

def fpow(function: Callable[[T], T], times: int) -> Callable[[T], T]:
    """Return a function that applies 'function' 'times' times

    >>> fpow(lambda x: 2*x, 4)(1)
    16
    """
    from itertools import repeat
    return fjoin(repeat(function, times))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
