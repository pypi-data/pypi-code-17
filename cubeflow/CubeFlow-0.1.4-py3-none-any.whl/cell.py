from typing import Tuple, Any, Dict, Sequence, Union


class Scalar(float):
    """
    Represents a floating point value within a cell that is also a integral part of a cell such as 
    velocity in a fluid-dynamics simulation. Scalar variables within a cell will be interpreted as data fields to
    output by cubeflow.report.Report instances opposed to helping variables, which are left behind. Note that 
    the MetaCell metaclass will convert all Scalar variables to builtin float variables at instance creation. 
    """
    def __init__(self) -> None:
        super().__init__()


class MetaCell(type):
    """
    Metaclass for all grid cell data types. MetaCell will search all class variables for variables of type Scalar 
    and construct __init__, __str__, values, items and names members accordingly. All variables of type Scalar will
    be replaced by variables of type float after instance creation. 
    >>> class Cell(metaclass=MetaCell):
    ...     value = Scalar()
    ...     position = Scalar()
    >>> c = Cell(0, value=2.0, position=1.0)
    >>> (c.value, c.position)
    (2.0, 1.0)
    >>> type(c.value).__name__
    'float'
    >>> c.type
    0
    >>> str(c)
    'Cell(position=1.0, type=0, value=2.0)'
    >>> c = Cell(type_=1)
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

        def items(self) -> Dict[str, float]:
            """
            Returns all former scalar values (see class Scalar for more details) and their values as a dictionary.
            :param self: 
            :return: Name to value mapping as dictionary ordered by name.
            """
            return dict([(field_name, getattr(self, field_name)) for field_name in self._args])

        cls.items = items

        def values(self) -> Sequence[Union[float, int]]:
            """
            Returns all scalar values (see class Scalar for more details).
            :param self: 
            :return: Values ordered by scalar name.
            """
            return [getattr(self, field_name) for field_name in self._args]

        cls.values = values

        def names(self) -> Sequence[str]:
            """
            Returns all scalar names (see class Scalar for more details).
            :param self: 
            :return: Scalar names in alphabetic order.
            """
            return [name for name in self._args]

        cls.names = names

        def update(self, other) -> None:
            """
            
            :param self: 
            :param other: 
            :return: 
            """
            for field_name in self._args:
                if field_name != 'type':
                    setattr(self, field_name, getattr(other, field_name))

        cls.update = update

        def __str__(self) -> str:
            """
            String representation of a cell, similar to a constructor call.
            :param self: 
            :return: Name(arg=value,...)
            """
            args = sorted(('{0}={1}'.format(*item) for item in self.items().items()))
            return '{0}({1})'.format(self.__class__.__name__, ', '.join(args))

        cls.__str__ = __str__



