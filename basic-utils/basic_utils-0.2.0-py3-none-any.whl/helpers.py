from collections import deque, abc, Iterable
from functools import reduce
from itertools import chain
from operator import getitem


def first(seq):
    """
    Returns first element in a sequence.

    >>> first([1, 2, 3])
    1
    """
    return next(iter(seq))


def rest(seq):
    """
    Returns remaining elements in a sequence

    >>> rest([1, 2, 3])
    [2, 3]
    """
    if isinstance(seq, (abc.Sequence, str)):
        return seq[1:]
    d = deque(seq)
    d.popleft()
    return tuple(d)


def last(seq):
    """
    Returns the last item in a sequence

    >>> last([1, 2, 3])
    3
    """
    if hasattr(seq, '__getitem__'):
        return seq[-1]
    return deque(iter(seq), maxlen=1).pop()


def butlast(seq):
    """
    Returns an iterable of all but the last item in the sequence

    >>> butlast([1, 2, 3])
    [1, 2]
    """
    if isinstance(seq, (abc.Sequence, str)):
        return seq[:-1]
    i = deque(seq)
    i.pop()
    return tuple(i)


def reverse(seq):
    """
    Returns a sequence of items in seq in reverse order

    >>> reverse([1, 2, 3])
    [3, 2, 1]
    """
    try:
        return seq[::-1]
    except TypeError:
        return tuple(y for y in reverse(list(seq)))


def partial_flatten(seq):
    """
    Returns partially flattened version of seq

    >>> list(flatten([[1, 2, 3], [4, 5, 6]]))
    [1, 2, 3, 4, 5, 6]
    """
    return type(seq)(chain.from_iterable(seq))


def flatten(seq):
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


def get_keys(obj, keys, default=None):
    """
    Returns multiple values for keys in a dictionary

    Empty key values will be None by default

    >>> d = {'x': 24, 'y': 25}
    >>> get_keys(d, ('x', 'y', 'z'))
    (24, 25, None)
    """
    return tuple(obj.get(key, default) for key in keys)


def dict_subset(d, keys, include_missing=True, default_key=None):
    """
    Returns a new dictionary with a subset of key value pairs from the original

    >>> d = {'a': 1, 'b': 2}
    >>> dict_subset(d, ('c',), True, 'missing')
    {'c': 'missing'}
    """
    new = {k: d.get(k, default_key) for k in keys}
    if include_missing:
        return new
    return {k: v for k, v in new.items() if v}


def get_in_dict(dict_in, keys):
    """
    Retrieve nested key from dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> get_in_dict(d, ('a', 'b', 'c'))
    3
    """
    return reduce(getitem, keys, dict_in)


def set_in_dict(dict_in, keys, value):
    """
    Sets a value inside a nested dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> set_in_dict(d, ('a', 'b', 'c'), 10)
    >>> d
    {'a': {'b': {'c': 10}}}
    """
    get_in_dict(dict_in, butlast(keys))[last(keys)] = value


def uniq(seq):
    """
    Removes duplicates from a sequence

    >>> uniq([1, 2, 1, 1, 2, 3])
    [1, 2, 3]
    """
    return type(seq)(set(seq))


def dedupe(items, key=None):
    """
    Removes duplicates from a sequence while maintaining order

    >>> list(dedupe([1, 5, 2, 1, 9, 1, 5, 10]))
    [1, 5, 2, 9, 10]
    """
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def prune_dict(d, key=lambda x: x is not None):
    """
    Returns new dictionary with key / values pairs filtered by key function.
    Prunes None values by default

    >>> d = {'Homer': 39, 'Marge': 36, 'Bart': 10}
    >>> prune_dict(d, key=lambda x: x < 20)
    {'Bart': 10}
    """
    return {k: v for k, v in d.items() if key(v)}
