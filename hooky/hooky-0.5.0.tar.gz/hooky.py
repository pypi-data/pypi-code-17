# coding=utf-8

from collections import MutableMapping, Sequence

import copy

__version__ = '0.5.0'


class Hook(object):
    def _before_add(self, key, item):
        """
        before add a item to the object will call this method.

        example: obj[key] = item
        """

    def _after_add(self, key, item):
        """
        like _before_add, but after add.
        """

    def _before_del(self, key, item):
        """
        before delete a item from the object will call this method.

        example: del obj[key]
        """

    def _after_del(self, key, item):
        """
        like _before_del, but after del.
        """


class Check:
    def _add_check(self, key, value):
        pass

    def _del_check(self, key, value):
        pass


class Garud:

    def _add_garud(self, key, value):
        return key, value

    def _del_garud(self, key):
        return key


class List(Hook, Sequence):
    """
    list like.
    """

    def __init__(self, initlist=None, hook_when_init=True):
        """

        :param initlist: iterable object
        :param hook_when_init: run hook points when it is True
        """

        self._data = []

        if initlist:
            if hook_when_init:
                self.extend(initlist)
            else:
                self._data.extend(initlist)

    def __setitem__(self, i, item):  # x[i] = item, del and add

        if isinstance(i, slice):
            if not hasattr(item, '__contains__'):
                raise TypeError('can only assign an iterable')

            start, stop, step = i.indices(len(self))

            ########################################################
            if step == 1:
                for one in range(stop - start):
                    del self[start]

                _i = start
                for one in item:
                    self.insert(_i, one)
                    _i += 1

            else:

                if step > 1:
                    slice_size = (stop - start) // step

                    if 0 < (stop - start) % step < step:
                        slice_size += 1
                else:
                    slice_size = (start - stop) // abs(step)

                    if 0 < (start - stop) % abs(step) < abs(step):
                        slice_size += 1

                slice_size = 0 if slice_size < 0 else slice_size
                if slice_size != len(item):
                    raise ValueError('attempt to assign sequence of size {} to extended slice of size {}'.format(
                        len(item), slice_size
                    ))

                _i = start
                for one in item:
                    self[_i] = one
                    _i += step

        else:
            del self[i]
            self.insert(i, item)

    # all del action will be here
    def __delitem__(self, i):  # del x[i], del
        item = self[i]
        self._before_del(key=i, item=item)
        del self._data[i]
        self._after_del(key=i, item=item)

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add action will be here
    def insert(self, i, item):
        self._before_add(key=i, item=item)
        self._data.insert(i, item)
        self._after_add(key=i, item=item)

    def pop(self, i=-1):  # del
        x = self[i]
        del self[i]
        return x

    def remove(self, item):  # del
        i = self.index(item)
        del self[i]

    def clear(self):  # del
        for i in range(len(self)):
            self.pop()

    def extend(self, other):  # add
        for item in other:
            self.append(item)

    def __iadd__(self, other):  # x += y, add
        self.extend(other)
        return self

    def __imul__(self, n):  # x *= y, add
        if not isinstance(n, int):
            raise TypeError("can't multiply sequence by non-int of type '{}'".format(type(n)))

        if n <= 0:
            self.clear()

        if n == 1:
            pass

        elif n > 1:
            old_data = copy.copy(self._data)
            for time in range(n - 1):
                self.extend(old_data)

        return self

    def __getitem__(self, i): return self._data[i]

    def __len__(self): return len(self._data)

    def __repr__(self): return repr(self._data)

    def __lt__(self, other): return self._data < self.__cast(other)

    def __le__(self, other): return self._data <= self.__cast(other)

    def __eq__(self, other): return self._data == self.__cast(other)

    def __gt__(self, other): return self._data > self.__cast(other)

    def __ge__(self, other): return self._data >= self.__cast(other)

    def __cast(self, other):
        return other._data if isinstance(other, List) else other

    def reverse(self): self._data.reverse()

    def sort(self, *args, **kwds): self._data.sort(*args, **kwds)


class Dict(Hook, MutableMapping):
    def __init__(*args, **kwargs):
        if not args:
            raise TypeError("descriptor '__init__' of 'Dict' object "
                            "needs an argument")

        self, *args = args

        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))

        if args:
            dict_ = args[0]

        elif 'dict' in kwargs:
            dict_ = kwargs.pop('dict')
            import warnings
            warnings.warn("Passing 'dict' as keyword argument is deprecated",
                          PendingDeprecationWarning, stacklevel=2)
        else:
            dict_ = None

        self._data = {}

        if dict_ is not None:
            self.update(dict_)
        if len(kwargs):
            self.update(kwargs)

    # all set action will be here
    def __setitem__(self, key, item):
        if key in self.keys():
            del self[key]

        self._before_add(key=key, item=item)
        self._data[key] = item
        self._after_add(key=key, item=item)

    # all del action will be here
    def __delitem__(self, key):
        item = self[key]
        self._before_del(key=key, item=item)
        del self._data[key]
        self._after_del(key=key, item=item)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __len__(self): return len(self._data)

    def copy(self):
        if self.__class__ is Dict:
            return Dict(self._data.copy())
        import copy
        data = self._data
        try:
            self._data = {}
            c = copy.copy(self)
        finally:
            self._data = data
        c.update(self)
        return c
