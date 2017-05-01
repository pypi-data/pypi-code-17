# The usage is explained in the the file "tests.py"
# The only deficiency is that you are not allowed to use the following keywords as keys in your settings:
# 'set', 'get', 'pop', 'update', 'delete', 'keys'
# You should also avoid dunder keywords (of the form: __keyword__)
# otherwise, the sky is the limit ...

DEFAULT_VALUE = object()

class Settings(object):
    "Settings management class. See tests.py in package for usage examples"
    def __init__(self, ___dictionary=None, **opt):
        if not ___dictionary is None:
            self.__dict__.update(___dictionary)
        self.__dict__.update(opt)

    def set(self, key, value):
        self.__dict__[key] = value
        return value

    def get(self, key, default_value=DEFAULT_VALUE):
        if key in self.__dict__:
            return self.__dict__[key]
        elif default_value is DEFAULT_VALUE:
            raise Exception("Invalid Key Error: %s" % (key,))
        else:
            self.set(key, default_value)
            return default_value

    def pop(self, key, default_value=DEFAULT_VALUE):
        if key in self.__dict__:
            return self.__dict__.pop(key)
        elif default_value is DEFAULT_VALUE:
            raise Exception("Invalid Key Error: %s" % (key,))
        else:
            return default_value

    def delete(self, key):
        if key in self.__dict__:
            self.__dict__.__delitem__(key)

    def update(self, d=None, **kwargs):
        if not d is None:
            self.__dict__.update(d)
        self.__dict__.update(**kwargs)

    def keys(self):
        return self.__dict__.keys()

    def __iter__(self):
        return iter(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.set(key, value)

    def __str__(self):
        state = ["%s = %r" % (attribute, value) for (attribute,value) in sorted(self.__dict__.items())]
        return '\n'.join(state)

    def __repr__(self):
        state = ["%s=%r" % (attribute, value) for (attribute,value) in sorted(self.__dict__.items())]
        line = ', '.join(state)
        if len(line) > 150:
            line = line[0:150] + ' ...'
        return 'Settings(' + line + ')'

__all__ = [Settings]

