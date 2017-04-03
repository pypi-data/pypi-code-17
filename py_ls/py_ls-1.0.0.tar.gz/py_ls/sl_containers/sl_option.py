class Option(object):
    def __call__(self, *args, **kwargs):
        if args[0] is not None:
            return Some(args[0])
        else:
            return Nothing

    @property
    def is_empty(self):
        """
        :return: Whether @self is Nothing
        :rtype: bool
        """
        raise NotImplementedError("Override me")

    @property
    def get(self):
        """
        :return: If @self is Some returns the wrapped value, else raises Exception
        :rtype: Any
        """
        raise NotImplementedError("Override me")

    @property
    def is_defined(self):
        """
        :return: Whether @self is Some
        :rtype: bool
        """
        return not self.is_empty

    def collect(self, predicate, function):
        """
        :param predicate: a function that evaluates wrapped in Some value to bool
        :type predicate: (Any) -> bool
        :param function: a function that transforms wrapped in Some value into another value
        :type function: (Any) -> (Any)
        :return: Some[T] where T is the value wrapped by @self transformed by @function if value wrapped by @self
        satisfies @predicate or Nothing if @self is Nothing or value wrapped by @self does not pass predicate
        :rtype: Option
        """
        return self.filter(predicate).map(function)

    def get_or_else(self, default):
        """
        :type default: Any
        :return: @default if @self is Nothing or value wrapped by @self if @self is Some
        :rtype: Any
        """
        return default if self.is_empty else self.get

    @property
    def or_none(self):
        """
        :return: value wrapped by @self if @self is Some or None otherwise
        :rtype: Any
        """
        return self.get_or_else(None)

    def map(self, f):
        """
        :param f: a function that transforms wrapped in Some value into another value
        :type f: (Any) -> (Any)
        :return: Some(y) where y is the value wrapped by @self transformed by function @f if @self is Some,
            else Nothing
        :rtype: Some | Nothing
        """
        return Nothing if self.is_empty else Some(f(self.get))

    def flat_map(self, f):
        """
        :param f: a function that transforms wrapped in Some value into another value
        :type f: (Any) -> (Any)
        :return: y where y is the value wrapped by @self transformed by function @f if @self is Some, else Nothing
        :rtype: Some | Nothing
        """
        return Nothing if self.is_empty else f(self.get)

    def filter(self, f):
        """
        :param f: a function that evaluates value wrapped in Some into bool
        :type f: (Any) -> bool
        :return: @self if value wrapped by @self satisfies @f, Nothing otherwise
        :rtype: Some | Nothing
        """
        return self if (not self.is_empty and f(self.get)) else Nothing

    def filter_not(self, f):
        """
        :param f: a function that evaluates value wrapped in Some into bool
        :type f: (Any) -> bool
        :return: @self if value wrapped by @self does not satisfy @f, Nothing otherwise
        :rtype: Some | Nothing
        """
        return self if (self.is_empty or f(self.get)) else Nothing

    def contains(self, e):
        """
        :type f: (Any)
        :return: False if @self is Nothing or the value wrapped in @self is not equal to @e, True otherwise
        :rtype: Some | Nothing
        """
        return not self.is_empty and self.get == e

    def exists(self, f):
        """
        :type f: (Any) -> bool
        :return: False if @self is nothing or value wrapped in @self does not satisfy f, True otherwise
        :rtype: Some | Nothing
        """
        return not self.is_empty and f(self.get)

    def forall(self, f):
        """
        :type f: (Any) -> bool
        :return: True if @self is Nothing or value wrapped in @self satisfied @f, False otherwise
        :rtype: Some | Nothing
        """
        return self.is_empty or f(self.get)

    def foreach(self, f):
        """
        :param f: function that takes value wrapped by @self and do whatever
        :type f: (Any) -> (Any)
        """
        if self.is_defined:
            f(self.get)

    def or_else(self, other):
        """
        :param other: other Option instance wrapping anything or Nothing
        :type other: Option
        :return: @self if @self is not Nothing, Nothing otherwise
        :rtype: Some | Nothing
        """
        return other if self.is_empty else self

    def or_else_raise(self, exception):
        """
        :param exception: exception to raise
        :type exception: Exception
        :raises: raises exception if @self is Nothing, else returns @self
        :raise: Exception
        """
        if self.is_empty:
            raise exception
        else:
            return self


class Some(Option):
    def __init__(self, val):
        self.val = val

    @property
    def is_empty(self):
        """
        :rtype: bool
        """
        return False

    @property
    def get(self):
        """
        :return: Value that is wrapped by @self
        :rtype: Any
        """
        return self.val

    def __eq__(self, other):
        if isinstance(other, Some):
            return self.val == other.val
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Some(" + (str(self.val) if not isinstance(self.val, basestring) else "\"{}\"".format(self.val)) + ")"

    def __str__(self):
        return self.__repr__()


class NothingClass(Option):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(NothingClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @property
    def get(self):
        """
        Look at superclass doc.

        :raises: Exception
        """
        raise Exception("Get method on Nothing object.")

    @property
    def is_empty(self):
        """
        Look at superclass doc.

        :rtype: bool
        """
        return True

    def __eq__(self, other):
        if isinstance(other, NothingClass):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Nothing"

    def __str__(self):
        return self.__repr__()


Nothing = NothingClass()
Option = Option()
