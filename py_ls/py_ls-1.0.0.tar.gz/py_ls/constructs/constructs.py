class RaiseFactory():
    def __call__(self, *args, **kwargs):
        if len(args) != 1:
            raise Exception("Invalid arguments")
        else:
            return lambda: self._raise(args[0])

    def __lshift__(self, exc):
        return lambda _: self._raise(exc)

    def __lt__(self, other):
        return self._raise(other)

    def _raise(self, exc):
        raise exc


Raise = RaiseFactory()


class Eq(object):
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def __str__(self):
        return self.__class__.__name__ + "[" + \
               ", ".join([str(attr) + "=" + ("'" + str(value) + "'" if isinstance(value, basestring)else str(value))
                          for attr,
                              value in \
                          self.__dict__.iteritems()]) + "]"

    def __repr__(self):
        return self.__str__()
