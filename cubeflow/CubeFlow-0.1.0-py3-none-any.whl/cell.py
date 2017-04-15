from typing import Tuple, Any, Dict, Sequence, Union


class Scalar(float):
    def __init__(self) -> None:
        super().__init__()


class MetaCell(type):
    """
    >>> class Cell(metaclass=MetaCell):
    ...     value = Scalar()
    ...     position = Scalar()
    >>> c = Cell(value=2.0, position=1.0)
    >>> (c.value, c.position)
    (2.0, 1.0)
    >>> type(c.value).__name__
    'float'
    >>> c.type
    0
    >>> c = Cell(type=1)
    >>> (c.type, c.value)
    (1, 0.0)
    """
    def __init__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> None:
        super(MetaCell, cls).__init__(name, bases, namespace)

        cls._args = [name for (name, value) in cls.__dict__.items() if isinstance(value, Scalar)]
        cls._args = sorted(cls._args)
        cls._args.append("type")

        cls.type = 0

        def init(self, type_: int, **kwargs):
            self.type = type_
            for (kwarg, value) in kwargs.items():
                if kwarg not in self._args:
                    raise AttributeError("Unknown attribute: {0}".format(kwarg))
                else:
                    setattr(self, kwarg, value)

        cls.__init__ = init

        def items(self):
            return dict([(field_name, getattr(self, field_name)) for field_name in self._args])

        cls.items = items

        def values(self) -> Sequence[Union[float, int]]:
            return [getattr(self, field_name) for field_name in self._args]

        cls.values = values

        def names(self) -> Sequence[str]:
            return [name for name in self._args]

        cls.names = names

        def __str__(self) -> str:
            args = ('{0}={1}'.format(*item) for item in self.items())
            return '{0}({1})'.format(self.__class__.__name__, ','.join(args))

        cls.__str__ = __str__



