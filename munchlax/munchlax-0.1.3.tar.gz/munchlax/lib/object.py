class Object(object):
    """
    A class for creating an object representation of a dictionary.
    """
    def __init__(self, d):
        def bind(x):
            if isinstance(x, dict):
                return Object(x)
            else:
                return x

        for k in d:
            if isinstance(d[k], list):
                self.__dict__[k] = [bind(x) for x in d[k]]
            else:
                self.__dict__[k] = bind(d[k])