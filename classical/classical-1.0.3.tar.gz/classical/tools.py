"""
Various helpers for working with classes
"""

import sys
import types


PYTHON_GE_3_6 = sys.version_info >= (3, 6)


def partial_class(cls, name, *args, **kwargs):
    """
    Create a subclass of ``cls`` identical to the original
    except for its name and additional arguments passed to ``__init__``

    :param cls: the class to be subclassed
    :param name: name of the new class
    :param args: positional arguments for ``__init__``
    :param kwargs: keyword arguments for ``__init__``
    :return: a subclass of ``cls``

    Say you have
    ::

        class Square:
            def __init__(self, size, color=None):
                pass  # implementation goes here

    The 'standard' way to subclass with fixed argument values would be to
    ::

        class RedSquare1x1(Square):
            def __init__(self):
                super().__init__(1, color='red)

    Consider the less-verbose alternative:
    ::

        RedSquare1x1 = partial_class(Square, 'RedSquare1x1', 1, color='red)
    """
    def new_init(self, *_args, **_kwargs):
        cls.__init__(self, *(args + _args), **dict(kwargs, **_kwargs))

    new_init.__name__ = '__init__'

    return types.new_class(
        name, (cls,), exec_body=lambda ns: (ns.__setitem__('__init__', new_init))
    )


class PartialProperty:
    """
    A descriptor that returns a :func:`partial_class` of the owner class when accessed.

    Basically it allows a class to have attributes that are its own subclasses:
    ::

        class Tree:
            Peach = PartialProperty(fruit='peach')
            Pine = PartialProperty(fruit='cone')
            # both will return subclasses of Tree when accessed

            def __init__(self, fruit):
                self.fruit = fruit

        issubclass(Tree.Pine, Tree)  # True
        Tree.Pine().fruit  # 'cone'

    These properties can be used recursively in combination with each other:
    ::

        class Polygon:
            Blue = PartialProperty(color='blue')
            Pentagon = PartialProperty(sides=5)

            def __init__(self, color=None, sides=3):
                self.color = color
                self.sides = sides

        blue_pentagon = Polygon.Pentagon.Blue()
        # blue_pentagon.color == 'blue'
        # blue_pentagon.sides == 5
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._cls_map = {}
        self._name = None  # type: str
        self._owner = None  # type: type

    def __set_name__(self, owner: type, name: str):
        self._name = name
        self._owner = owner

    def _get_own_name(self, owner: type) -> str:
        try:
            own_name = [
                name for name, attr in owner.__dict__.items()
                if attr is self
            ][0]
        except IndexError:
            own_name = None
            for base in owner.__bases__:
                own_name = self._get_own_name(base)
                break

            if not own_name:
                raise RuntimeError('Property is not bound to any class')

        return own_name

    def __get__(self, instance, owner):
        if self._name is None:  # has not been set yet
            # get the name of the attribute - it will serve as the name
            # of the new partial class
            own_name = self._get_own_name(owner)
            self.__set_name__(owner=owner, name=own_name)

        if owner not in self._cls_map:
            self._cls_map[owner] = partial_class(owner, self._name, *self.args, **self.kwargs)

        return self._cls_map[owner]


class AutoProperty:
    """
    A descriptor that returns an instance of the owner class when accessed.

    The instance is created with the custom arguments
    that are passed to the property's constructor.

    Acts somewhat like an ``Enum``
    ::

        class Thing:
            book = AutoProperty(color='brown', size=5)
            pencil = AutoProperty(color='green', size=1)
            # both will return instances of Thing when accessed

            def __init__(self, color, size):
                self.color = color
                self.size = size

        isinstance(Thing.book, Thing)  # True
        Thing.book.color  # 'brown'
        Thing.book is Thing.book  # True (the same instance is returned every time)

    These properties can be used in a subclass to produce instances of the subclass:
    ::

        class ClassyThing(Thing):
            pass

        isinstance(ClassyThing.book, ClassyThing)  # True
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._cls_map = {}

    def __get__(self, instance, owner):
        if owner not in self._cls_map:
            self._cls_map[owner] = owner(*self.args, **self.kwargs)

        return self._cls_map[owner]
