# -*- coding: utf-8 -*-
from operator import itemgetter, attrgetter

from accessor.exceptions import ResolverException
from accessor.utils import indexgetter


class Accessor(object):
    """
    Utility to resolve path on an object. Example:
    
    > obj = [{'a': 'abc'}, 1]
    > a = Accessor('0.a.upper')
    > a.resolve(obj)
    'ABC'
    """
    delimiter = '.'
    fail_silently = True
    call = True
    resolvers = (
        (itemgetter, (TypeError, AttributeError, KeyError)),
        (attrgetter, (TypeError, AttributeError)),
        (indexgetter, (TypeError, TypeError, ValueError, KeyError))
    )

    def __init__(self, path):
        self.path = path

    @property
    def bits(self):
        if self.path == '':
            return ()
        return self.path.split(self.delimiter)

    def resolve(self, obj):
        current = obj
        for bit in self.bits:
            try:
                current = self.__resolve_bit(current, bit)
            except ResolverException:
                if not self.fail_silently:
                    self.__fail(bit, current, obj)
                return None
        if self.check_callable(current):
            current = current()
        return current

    def __resolve_bit(self, obj, bit):
        for resolver, exceptions in self.resolvers:
            try:
                return resolver(bit)(obj)
            except exceptions:
                pass
        raise ResolverException()

    def __fail(self, bit, current, obj):
        raise ValueError(
            u'Failed lookup for bit "{bit}" in "{cur}" when resolving "{acc}" for "{obj}"'.format(
                bit=bit, cur=current, acc=self, obj=obj))

    def check_callable(self, current):
        """
        Hook to check whether it is safe and appropriate to call the current context object.
        
        :param current: Current context object 
        :return: True if it is safe and appropriate to call `current()`
        """
        return self.call and callable(current)

    def __str__(self):
        return self.path


A = Accessor


class NonCallingAccessor(Accessor):
    call = False


class FailLoudAccessor(Accessor):
    fail_silently = False


if __name__ == '__main__':
    obj = [{'a': 'abc'}, 1]
    a = Accessor('0.a.upper')
    print(a.resolve(obj))
