from .base import Base


class KeyOption(Base):
    def __init__(self, name):
        self.name = self.value = name

    def __repr__(self):
        return self._render(
            '{name};'.format(
                name=self.name,
            )
        )


class KeyValueOption(Base):
    def __init__(self, name, value=''):
        self.name = name
        if isinstance(value, bool):
            self.value = 'off' if value is False else 'on'
        elif isinstance(value, int):
            self.value = str(value)
        elif isinstance(value, list):
            self.value = [str(e) for e in value]
        else:
            self.value = value

    def __repr__(self):
        return self._render(
            '{name} {value};'.format(
                name=self.name,
                value=self.value
            )
        )


class KeyMultiValueOption(KeyValueOption):
    def __repr__(self):
        return self._render(
            '{name} {value};'.format(
                name=self.name,
                value=' '.join(self.value)
            )
        )


class Comment(Base):
    _offset = ''
    _comment = ''

    def __init__(self, offset='', comment='', **kwargs):
        self._offset = offset
        self._comment = comment
        super(Comment, self).__init__(**kwargs)

    def __repr__(self):
        return self._render(
            '{offset}# {comment}'.format(
                offset=self._offset,
                comment=self._comment,
            )
        )


class AttrDict(dict):
    def __init__(self, owner):
        self.__dict__ = self
        self._owner = owner

    def __setitem__(self, key, val):
        if hasattr(val, '_parent'):
            val._parent = self._owner
        return super(AttrDict, self).__setitem__(key, val)

    def __repr__(self):
        owner = self.pop('_owner')
        ret = super(AttrDict, self).__repr__()
        self._owner = owner
        return ret


class AttrList(AttrDict):
    def __iter__(self):
        return iter(self.values())

    def append(self, item):
        if hasattr(item, '_parent'):
            item._parent = self._owner
        if hasattr(item, 'name'):
            self[item.name] = item
        else:
            self[hash(item)] = item

    def add(self, *items):
        for item in items:
            self.append(item)
