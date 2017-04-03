from sl_option import Nothing, Some


class Try(object):
    """
        Abstraction over Try-except blocks.
        Represent a computation that can success or throw an Exception
    """

    @staticmethod
    def fail(message):
        return Failure(Exception(message))

    def __call__(self, *args, **kwargs):
        try:
            return Success(args[0]())
        except Exception as e:
            return Failure(e)

    @property
    def get_exc(self):
        """
        Retrieves the exception thrown by computation passed to Try.

        :rtype: Exception
        """
        raise NotImplementedError()

    @property
    def is_success(self):
        """
        Whether passed computation resulted in a correct value and no exception was thrown

        :rtype: boolean
        """
        raise NotImplementedError()

    @property
    def is_failure(self):
        """
        Whether passed computation resulted in an exception thrown

        :rtype: boolean
        """
        return not self.is_success

    @property
    def get(self):
        raise NotImplementedError()

    @property
    def failed(self):
        """
        Inverts the result of a computation.
        If it resulted in a Failure, returns Success wrapping the exception
        If it resulted in a Success, returns a Failure wrapping a RuntimeError

        :rtype: slpy.sl_collections.sl_cont.Try
        """
        if self.is_failure:
            return Success(self.val)
        else:
            return Failure(RuntimeError("Inverted on Success"))

    def filter(self, f):
        """
        On Failure returns the Failure itself.
        On Success, checks if computation result matches @f. If it does, returns Success itself.
        Otherwise, returns Failure.

        :type f: (x) -> bool
        :rtype: slpy.sl_collections.sl_cont.Try
        """
        if self.is_failure:
            return self
        else:
            if not f(self.get):
                return Failure(Exception("Predicate does not hold for {}".format(self.get)))
            else:
                return Success(self.get)

    def get_or_else(self, default):
        """
        On Failure returns the @default.
        On Success, retrieves the computation result.

        :type default: Any
        :rtype: slpy.sl_collections.sl_cont.Try
        """

        return self.get if self.is_success else default

    def map(self, f):
        """
        Mapping a Try that is a Success will result in a Success with value mapped by @f.
        If it's a Failure, then resulting Try will be the same failure instance.

        :type f: (x) -> Any
        :rtype: sl_py.sl_containers.sl_try.Try
        """
        if self.is_failure:
            return Failure(self.get_exc)
        else:
            return Try(lambda: f(self.get))

    def flat_map(self, f):
        """
        Flat mapping a Try that is a Success will result in a Success with value mapped by @f.
        If it's a Failure, then resulting Try will be the same failure instance.

        :type f: (x) -> Any
        :rtype: slpy.sl_collections.sl_cont.Try.
        """
        if self.is_failure:
            return Failure(self.get_exc)
        else:
            return f(self.get)

    def foreach(self, side_eff_function):
        if self.is_failure:
            pass
        else:
            side_eff_function(self.get)

    def recover(self, f):
        if self.is_failure:
            return Try(lambda: f(self.get_exc))
        else:
            return self

    def transform(self, s, f):
        if self.is_failure:
            return f(self.get_exc)
        else:
            return s(self.get)

    @property
    def option(self):
        return Nothing if self.is_failure else Some(self.get)

    def __eq__(self, other):
        if isinstance(other, Failure):
            return self.val == other.val
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Success(Try):
    def __init__(self, val):
        self.val = val

    @property
    def is_success(self):
        """
        Whether passed computation resulted in a correct value and no exception was thrown

        :rtype: boolean
        """
        return True

    @property
    def get(self):
        """
        Returns the value retrieved from invoking a computation passed to Try.

        :rtype: Any
        """
        return self.val

    @property
    def get_exc(self):
        """
        Retrieves the exception thrown by computation passed to Try.

        :rtype: Exception
        """
        raise RuntimeError("get_exc on Success")

    def __repr__(self):
        return "Success(" + str(self.val) + ")"

    def __str__(self):
        return "Success(" + str(self.val) + ")"


class Failure(Try):
    def __init__(self, val):
        self.val = val

    @property
    def is_success(self):
        """
        Whether passed computation resulted in a correct value and no exception was thrown

        :rtype: boolean
        """
        return False

    @property
    def get(self):
        """
        Raises an exception if the computation passed to Try resulted in failure.

        :raise: Exception
        """
        raise self.val

    @property
    def get_exc(self):
        """
        Retrieves the exception thrown by computation passed to Try.

        :rtype: Exception
        """
        return self.val

    def __repr__(self):
        return "Failure(\"" + str(self.val.message) + "\")"

    def __str__(self):
        return "Failure(\"" + str(self.val.message) + "\")"


Try = Try()
