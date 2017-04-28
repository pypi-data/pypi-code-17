import os
from collections import defaultdict
from functools import reduce
from itertools import chain
from operator import attrgetter
from typing import Any, List, Sequence, Tuple

__all__ = [
    'clear', 'getattrs', 'map_getattr', 'recursive_default_dict', 'rgetattr',
    'rsetattr', 'slurp', 'to_string',
]


def slurp(fname: str) -> str:
    """
    Reads a file and all its contents, returns a single string
    """
    with open(fname, 'r') as f:
        data = f.read()
    return data


def clear() -> None:
    """
    Clears the terminal screen from python, operating system agnostic
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def to_string(objects: List[object], sep: str = ", ") -> str:
    """
    Converts a list of objects into a single string

    >>> to_string([1, 2, 3])
    '1, 2, 3'
    """
    return sep.join(map(str, objects))


def getattrs(obj: object, keys: Sequence[str]) -> Tuple[Any, ...]:
    """Supports getting multiple attributes from a model at once"""
    return tuple(getattr(obj, key) for key in keys)


def map_getattr(attr: str, object_seq: Sequence[object]) -> Tuple[Any, ...]:
    """
    Returns a map to retrieve a single attribute from a sequence of objects
    """
    return tuple(map(attrgetter(attr), object_seq))


def recursive_default_dict() -> defaultdict:
    """Returns a default dict that points to itself"""
    return defaultdict(recursive_default_dict)


def rgetattr(obj: object, attrs: str) -> Any:
    """Get a nested attribute within an object"""
    return reduce(getattr, chain([obj], attrs.split('.')))


def rsetattr(obj: object, attr: str, val: Any) -> None:
    """Sets a nested attribute within an object"""
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)
