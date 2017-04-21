from collections import defaultdict
from functools import reduce

import operator
import os

sentinel = object()


def slurp(fname):
    """
    Reads a file and all its contents, returns a single string
    """
    with open(fname, 'r') as f:
        data = f.read()
    return data


def clear():
    """
    Clears the terminal screen from python, operating system agnostic
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def to_string(objects, sep=", "):
    """
    Converts a list of objects into a single string

    >>> to_string([1, 2, 3])
    '1, 2, 3'
    """
    return sep.join([(str(obj)) for obj in objects])


def getattrs(obj, keys):
    """Supports getting multiple attributes from a model at once"""
    return tuple(getattr(obj, k) for k in keys)


def map_getattr(attr, object_seq):
    """
    Returns a map to retrieve a single attribute from a sequence of objects
    """
    return tuple(map(operator.attrgetter(attr), object_seq))


def recursive_default_dict():
    """Returns a default dict that points to itself"""
    return defaultdict(recursive_default_dict)


def rgetattr(obj, attrs, default=sentinel):
    """Get a nested attribute within an object"""
    return reduce(getattr, [obj] + attrs.split('.'))


def rsetattr(obj, attr, val):
    """Sets a nested attribute within an object"""
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def identity(*args):
    """
    Returns the same values passed as arguments

    >>> identity(10, 20)
    (10, 20)
    """
    first, *rest = args
    return first if not rest else args
