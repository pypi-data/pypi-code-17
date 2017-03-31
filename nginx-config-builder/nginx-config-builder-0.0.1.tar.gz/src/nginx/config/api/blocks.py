import six

from .base import Base
from .options import AttrDict, AttrList, KeyOption, KeyValueOption, KeyMultiValueOption


class Block(Base):
    def __init__(self, name, *sections, **options):
        self.name = name
        self.sections = AttrList(self)
        self.options = AttrDict(self)

        self._set_directives(*sections, **options)

    @property
    def _directives(self):
        dirs = self._dump_options() + list(self.sections)
        return [directive for directive in dirs if directive is not self]

    def _set_directives(self, *sections, **options):
        for section in sections:
            self.sections.append(section)
        for key, value in six.iteritems(options):
            setattr(self.options, key, value)

    def _build_options(self, key, value):
        if isinstance(value, Block):
            option = value
        elif isinstance(value, list):
            option = KeyMultiValueOption(key, value=value)
        elif value is None or value == '':
            option = KeyOption(key)
        else:
            if isinstance(value, str) and ' ' in value:
                option = KeyMultiValueOption(key, value=value.split())
            else:
                option = KeyValueOption(key, value=value)
        return option

    def _dump_options(self):
        return [self._build_options(key, value) for key, value in six.iteritems(self.options)]

    def __repr__(self):
        directives = self._directives

        for directive in directives:
            if directive is not self:
                directive._indent_level = self._indent_level + 1

        return '\n{indent}{name}{{{directives}\n{indent}}}'.format(
            name='{0} '.format(self.name),
            directives=''.join([repr(e) for e in directives]),
            indent=self._get_indent(),
        )


class EmptyBlock(Block):
    def __init__(self, *sections, **options):
        self.sections = AttrList(self)
        self.options = AttrDict(self)

        self._set_directives(*sections, **options)

    def __repr__(self):
        directives = self._directives

        for directive in directives:
            directive._indent_level = self._indent_level

        return ''.join([repr(o) for o in directives])


class Location(Block):
    def __init__(self, location, *args, **kwargs):
        super(Location, self).__init__('location {0}'.format(location), *args, **kwargs)
