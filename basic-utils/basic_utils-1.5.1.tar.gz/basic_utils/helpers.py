from functools import reduce
from itertools import chain
from operator import getitem
from typing import Any, Callable, Iterable, Sequence, Tuple

__all__ = [
    'butlast', 'concat', 'cons', 'dedupe', 'dict_subset', 'first', 'flatten',
    'get_keys', 'getitem', 'head', 'init', 'last', 'partial_flatten',
    'prune_dict', 'rest', 'reverse', 'set_in_dict', 'tail',
]


def first(seq: Sequence) -> Any:
    """
    Returns first element in a sequence.

    >>> first([1, 2, 3])
    1
    """
    return next(iter(seq))


def second(seq: Sequence) -> Any:
    """
    Returns second element in a sequence.

    >>> second([1, 2, 3])
    2
    """
    return seq[1]


def last(seq: Sequence) -> Any:
    """
    Returns the last item in a Sequence

    >>> last([1, 2, 3])
    3
    """
    return seq[-1]


def butlast(seq: Sequence) -> Sequence:
    """
    Returns all but the last item in sequence

    >>> butlast([1, 2, 3])
    [1, 2]
    """
    return seq[:-1]


def rest(seq: Sequence) -> Any:
    """
    Returns remaining elements in a sequence

    >>> rest([1, 2, 3])
    [2, 3]
    """
    return seq[1:]


def reverse(seq: Sequence) -> Sequence:
    """
    Returns sequence in reverse order

    >>> reverse([1, 2, 3])
    [3, 2, 1]
    """
    return seq[::-1]


def cons(item: Any, seq: Sequence) -> chain:
    """ Adds item to beginning of sequence.

    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    return chain([item], seq)


def flatten(seq: Iterable) -> Iterable:
    """
    Returns a generator object which when evalutated
    returns a flatted version of seq

    >>> list(flatten([1, [2, [3, [4, 5], 6], 7]]))
    [1, 2, 3, 4, 5, 6, 7]
    """
    for item in seq:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


def partial_flatten(seq: Iterable) -> Iterable:
    """
    Returns partially flattened version of seq

    >>> list(flatten([[1, 2, 3], [4, 5, 6]]))
    [1, 2, 3, 4, 5, 6]
    """
    return chain.from_iterable(seq)


def dedupe(seq: Sequence, key: Callable=None) -> Iterable:
    """
    Removes duplicates from a sequence while maintaining order

    >>> list(dedupe([1, 5, 2, 1, 9, 1, 5, 10]))
    [1, 5, 2, 9, 10]
    """
    seen = set()  # type: set
    for item in seq:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def get_keys(d: dict, keys: Sequence[str], default: Callable=None) -> Tuple:
    """
    Returns multiple values for keys in a dictionary

    Empty key values will be None by default

    >>> d = {'x': 24, 'y': 25}
    >>> get_keys(d, ('x', 'y', 'z'))
    (24, 25, None)
    """
    return tuple(d.get(key, default) for key in keys)


def dict_subset(d, keys, prune=False, default=None):
    # type: (dict, Sequence[str], bool, Callable) -> dict
    """
    Returns a new dictionary with a subset of key value pairs from the original

    >>> d = {'a': 1, 'b': 2}
    >>> dict_subset(d, ('c',), True, 'missing')
    {'c': 'missing'}
    """
    new = {k: d.get(k, default) for k in keys}
    if prune:
        return prune_dict(new)
    return new


def get_in_dict(d: dict, keys: Sequence[str]) -> Any:
    """
    Retrieve nested key from dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> get_in_dict(d, ('a', 'b', 'c'))
    3
    """
    return reduce(getitem, keys, d)


def set_in_dict(d: dict, keys: Sequence[str], value: Any) -> None:
    """
    Sets a value inside a nested dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> set_in_dict(d, ('a', 'b', 'c'), 10)
    >>> d
    {'a': {'b': {'c': 10}}}
    """
    get_in_dict(d, butlast(keys))[last(keys)] = value


def prune_dict(d: dict, key: Callable=lambda x: x is not None) -> dict:
    """
    Returns new dictionary with values filtered by key fn.
    Prunes None values by default

    >>> d = {'Homer': 39, 'Marge': 36, 'Bart': 10}
    >>> prune_dict(d, key=lambda x: x < 20)
    {'Bart': 10}
    """
    return {k: v for k, v in d.items() if key(v)}


# Define some common aliases
head = first
tail = rest
init = butlast
concat = chain
