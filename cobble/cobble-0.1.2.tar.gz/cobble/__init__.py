import itertools
import functools
import abc
import inspect

from .six import exec_, iteritems
from . import six
from .inflection import underscore


def data(cls):
    fields = sorted(
        filter(
            None,
            map(functools.partial(_read_field, cls), dir(cls))
        ),
        key=lambda field: field[1].sort_key
    )
    _add_methods(cls, _methods(cls, fields))
    visitable(cls)
    cls._cobble_fields = fields
    return cls

def _add_methods(cls, methods):
    definitions = _compile_definitions(methods, {cls.__name__: cls})
    for key, value in iteritems(definitions):
        setattr(cls, key, value)
    

def _methods(cls, fields):
    names = [name for name, field in fields]
    return [
        _make_init(cls, fields),
        _make_repr(cls, names),
        _make_eq(cls, names),
        _make_neq(),
        _make_hash(cls, names),
    ]


def _make_init(cls, fields):
    def make_arg(name, field):
        if field.default == _undefined:
            return name
        else:
            return "{0}={1}".format(name, field.default)
    
    args_source = ", ".join(make_arg(name, field) for name, field in fields)
    assignments_source = "".join(
        "\n    self.{0} = {0}".format(name)
        for name, field in fields
    )
    return "def __init__(self, {0}):{1}\n    super({2}, self).__init__()\n".format(args_source, assignments_source, cls.__name__)


def _make_repr(cls, names):
    return "def __repr__(self):\n     return '{0}({1})'.format({2})\n".format(
        cls.__name__,
        ", ".join("{0}={{{1}}}".format(name, index) for index, name in enumerate(names)),
        ", ".join("repr(self.{0})".format(name) for name in names)
    )


def _make_eq(cls, names):
    conditions = ["isinstance(other, {0})".format(cls.__name__)] + \
        ["self.{0} == other.{0}".format(name) for name in names]
    return "def __eq__(self, other):\n    return {0}".format(" and ".join(conditions))


def _make_neq():
    return "def __ne__(self, other): return not (self == other)"


def _make_hash(cls, names):
    elements = [cls.__name__] + ["self.{0}".format(name) for name in names]
    return "def __hash__(self): return hash(({0}))".format(", ".join(elements))


def _make_accept(cls):
    return "def _accept(self, visitor): return visitor.{0}(self)".format(_visit_method_name(cls))


_sort_key_count = itertools.count()
_undefined = object()


def field(default=_undefined):
    if default not in [_undefined, None]:
        raise TypeError("default value must be None")
    return _Field(next(_sort_key_count), default=default)


class _Field(object):
    def __init__(self, sort_key, default):
        self.sort_key = sort_key
        self.default = default


def _read_field(cls, name):
    member = getattr(cls, name)
    if isinstance(member, _Field):
        return name, member
    else:
        return None

_visitables = set()

def visitable(cls):
    _visitables.add(cls)
    _add_methods(cls, [_make_accept(cls)])
    return cls


def visitor(cls):
    abstract_method_template = """
    @abc.abstractmethod
    def {0}(self, value):
        pass
"""
    abstract_methods = (
        abstract_method_template.format(_visit_method_name(subclass))
        for subclass in _subclasses(cls)
        if subclass in _visitables
    )
    
    if six.PY2:
        py2_metaclass = "__metaclass__ = abc.ABCMeta"
        py3_metaclass = ""
    else:
        py2_metaclass = ""
        py3_metaclass = ", metaclass=abc.ABCMeta"
    
    source = """
class {0}Visitor(object{1}):
    {2}

    def visit(self, value):
        return value._accept(self)
    
{3}
""".format(cls.__name__, py3_metaclass, py2_metaclass, "\n".join(abstract_methods))
    definition = _compile_definitions([source], {abc: abc})
    return next(iter(definition.values()))


def _compile_definitions(definitions, bindings):
    definition_globals = {"abc": abc}
    definition_globals.update(bindings)
    stash = {}
    exec_("\n".join(definitions), definition_globals, stash)
    return stash

def _visit_method_name(cls):
    return "visit_" + underscore(cls.__name__)


def _subclasses(cls):
    subclasses = cls.__subclasses__()
    index = 0
    while index < len(subclasses):
        subclasses += _subclasses(subclasses[index])
        index += 1
    return subclasses


def copy(obj, **kwargs):
    obj_type = type(obj)
    attrs = dict(
        (name, getattr(obj, name))
        for name, field in obj_type._cobble_fields
    )
    attrs.update(kwargs)
    return type(obj)(**attrs)
