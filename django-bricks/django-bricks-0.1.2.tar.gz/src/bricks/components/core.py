import abc
import collections
import copy

from markupsafe import Markup

from bricks.components import Attrs, Children
from bricks.components.mixins import HasParentMixin
from bricks.helpers import render_tag
from bricks.mixins import Renderable
from bricks.require import RequirableMeta, Requirable
from bricks.utils import dash_case
from bricks.request import request


class MetaInfo:
    """
    MetaInfo is the base class for the _meta attribute of components.
    """

    children_factory = Children
    attrs_factory = Attrs
    _valid_vars = {var for var in locals() if not var.startswith('_')}

    def __init__(self, meta):
        names = [x for x in dir(meta) if not x.startswith('_')]
        for name in names:
            if name not in self._valid_vars:
                raise AttributeError('invalid variable for Meta: %r' % name)
            setattr(self, name, getattr(meta, name))


class ComponentMeta(RequirableMeta, abc.ABCMeta):
    """
    Metaclass for Element and HTMLTag classes.
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if 'tag_name' not in namespace:
            for subclass in reversed(cls.mro()[1:]):
                if (hasattr(subclass, 'tag_name') and
                            subclass.tag_name != dash_case(subclass.__name__)):
                    break
            else:
                cls.tag_name = dash_case(name)

    def __getitem__(cls, item):
        obj = cls()
        return obj[item]


class BaseComponent(HasParentMixin,
                    Requirable,
                    Renderable, metaclass=ComponentMeta):
    """
    Common functionality to Element and Tag
    """

    def __init__(self, data=None, class_=None, id=None, attrs=None,
                 parent=None, **kwargs):
        Requirable.__init__(self)
        self.id = id
        if isinstance(class_, str):
            self.classes = class_.split()
        elif class_ is None:
            self.classes = []
        else:
            self.classes = list(class_)

        self.attrs = Attrs(self, attrs or {})
        self.attrs.update(**kwargs)

        HasParentMixin.__init__(self, parent)
        self.children = Children(self)
        if data is None:
            pass
        elif isinstance(data, (str, Markup, BaseComponent)):
            self.children.append(data)
        elif isinstance(data, collections.Iterable):
            self.children.extend(data)
        else:
            self.children.append(data)

    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            self.children.extend([x for x in item if x is not None])
        elif item is not None:
            self.children.append(item)
        return self

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            if self.classes != other.classes:
                return False
            if self.attrs != other.attrs:
                return False
            if len(self.children) != len(other.children):
                return False
            if any(x != y for (x, y) in zip(self.children, other.children)):
                return False
            return True
        return NotImplemented

    def __repr__(self):
        name = self.__class__.__name__
        if not self.attrs and not self.children:
            return '%s()' % name
        elif self.attrs and not self.children:
            return '%s(%s)' % (name, self.attrs._as_inner_repr())
        elif not self.attrs and self.children:
            fmt = '%s(%s)' if len(self.children) == 1 else '%s([%s])'
            return fmt % (name, self.children._as_inner_repr())
        else:
            fmt = (name, self.attrs._as_inner_repr(),
                   self.children._as_inner_repr())
            return '%s(%s)[%s]' % fmt

    def copy(self, parent=None, keep_id=False):
        """
        Return a copy of object, possibly setting a new parent.

        Id is not the same.
        """

        new = copy.copy(self)
        new._parent = None
        new.parent = parent
        new.attrs = self.attrs.copy(new)
        new.children = type(self.children)(new)
        new.children.extend([child.copy() for child in self.children])
        new.classes = self.classes.copy()
        if keep_id:
            new.id = self.id
        return new

    def add_class(self, cls, *extra_classes):
        """
        Add classes to the class list.

        Does nothing if class is already present.
        """

        if cls not in self.classes:
            self.classes.append(cls)
        if extra_classes:
            cls_set = set(self.classes)
            classes = [cls for cls in extra_classes if cls not in cls_set]
            self.classes.extend(classes)

    def render(self, request, id=None, cls=None, **kwargs):
        """
        Renders element as HTML.
        """

        content = self.children.render(request, **kwargs)
        return render_tag(self.tag_name, content, self.attrs, request=request)

    def json(self, **kwargs):
        """
        JSON representation of object.
        """

        json = {'tag': self.tag_name}
        if self.classes:
            json['classes'] = list(self.classes)
        if self.id is not None:
            json['id'] = self.id
        if self.attrs.has_own_attrs():
            json['attrs'] = self.attrs.own_attrs()
        if self.children:
            json['children'] = [x.json() for x in self.children]
        return json


class Component(BaseComponent):
    """
    Base class for all custom elements.
    """


class Tag(BaseComponent):
    """
    Base class for all HTML tag elements.
    """


class SelfClosingTag(Tag):
    """
    Base class for self closing tags such as <input>, <br>, <meta>, etc.
    """
