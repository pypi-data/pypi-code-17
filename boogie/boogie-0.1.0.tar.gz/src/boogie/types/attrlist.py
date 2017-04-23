import collections


class AttrList(collections.MutableSequence):
    """
    A list-like object that also accepts attribute access from the given list
    of fields.
    """
    __slots__ = ('fields', '_cache', '_data')

    def __init__(self, data, fields=()):
        self.fields = tuple(fields)
        self._cache = {}
        self._data = data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        return self._data[idx]

    def __setitem__(self, idx, value):
        self._data[idx] = value

    def __delitem__(self, idx):
        del self._data[idx]
        field = self.fields.pop(idx)
        self._cache.pop(field, None)

    def __getattr__(self, attr):
        try:
            idx = self._cache[attr]
        except KeyError:
            try:
                self._cache[attr] = idx = self.fields.index(attr)
            except ValueError:
                raise AttributeError(attr)
        return self._data[idx]

    def __repr__(self):
        return repr(self._data)

    def __eq__(self, other):
        if isinstance(other, (AttrList, list)):
            if len(other) != len(self):
                return False
            return all(x == y for x, y in zip(self, other))
        return NotImplemented

    def __add__(self, other):
        return self._data.__add__(other)

    def __radd__(self, other):
        return self._data.__radd__(other)

    def __mul__(self, other):
        return self._data.__mul__(other)

    def __rmul__(self, other):
        return self._data.__rmul__(other)

    def insert(self, idx, value):
        self._data.insert(idx, value)
        self.fields.insert(idx, None)
        self._cache.clear()