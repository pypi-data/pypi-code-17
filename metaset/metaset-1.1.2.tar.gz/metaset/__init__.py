# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from copy import deepcopy
from pkg_resources import get_distribution


__version__ = get_distribution('metaset').version


class MetaSet(dict):
    """Basically a dict of set-like objects that behaves as a set.
    Inception is possible.

    Note keys are conserved, even when their content becomes empty.
    They are not conserved in the intersection case,
    if they are not on both ends of the intersection.

    Examples:

    >>> MetaSet(a={1, 2}) & MetaSet(b={3})
    {}
    >>> MetaSet(a={1, 2}) & MetaSet(a={3, 4}, b={1})
    {'a': set()}
    >>> MetaSet(a={1}) - MetaSet(a={1, 2})
    {'a': set()}
    >>> MetaSet(a={1}) ^ MetaSet(a={1, 2})
    {'a': {2}}

    These are less expected:

    >>> MetaSet(a=set()) - MetaSet(a=set())
    {'a': set()}
    >>> MetaSet(a={1}) ^ MetaSet(a={1})
    {'a': set()}
    >>> MetaSet(a=set()) ^ MetaSet(a=set())
    {'a': set()}

    But note symmetric difference has to be permutable:

    >>> MetaSet(a={1}) ^ MetaSet(a={1}) ^ MetaSet(a=set())
    {'a': set()}
    >>> MetaSet(a={1}) ^ MetaSet(a=set()) ^ MetaSet(a={1})
    {'a': set()}

    Finally you can use inception, and this is where key conservation kicks in:

    >>> from pprint import pprint  # for doctest
    >>> pprint(MetaSet(a=MetaSet(b={1, 2}), c=MetaSet(d={3})))
    {'a': {'b': {1, 2}}, 'c': {'d': {3}}}
    >>> MetaSet(a=MetaSet(b={1}), c=MetaSet(d={3})) & MetaSet(a=MetaSet(b={4}))
    {'a': {'b': set()}}
    """
    @classmethod
    def from_dict(cls, value):
        try:
            return cls({k: cls.from_dict(v) for k, v in value.items()})
        except AttributeError:
            return set(value)

    def __isub__(self, rhs):
        for k, v in rhs.items():
            if k in self:
                self[k] -= v
        return self

    def __iand__(self, rhs):
        for k, v in rhs.items():
            if k in self:
                self[k] &= v
        for k in set(self.keys()) - set(rhs.keys()):
            del self[k]
        return self

    def __ixor__(self, rhs):
        for k, v in rhs.items():
            if k in self:
                self[k] ^= v
            else:
                self[k] = v
        return self

    def __ior__(self, rhs):
        for k, v in rhs.items():
            if k in self:
                self[k] |= v
            else:
                self[k] = v
        return self

    def __sub__(self, rhs):
        ret = deepcopy(self)
        ret -= rhs
        return ret

    def __and__(self, rhs):
        ret = deepcopy(self)
        ret &= rhs
        return ret

    def __xor__(self, rhs):
        ret = deepcopy(self)
        ret ^= rhs
        return ret

    def __or__(self, rhs):
        ret = deepcopy(self)
        ret |= rhs
        return ret

    def __lt__(self, rhs):
        return all(k in rhs and v < rhs[k] for k, v in self.items())

    def __le__(self, rhs):
        return all(k in rhs and v <= rhs[k] for k, v in self.items())

    def __gt__(self, rhs):
        return all(k not in rhs or v > rhs[k] for k, v in self.items())

    def __ge__(self, rhs):
        return all(k not in rhs or v >= rhs[k] for k, v in self.items())
