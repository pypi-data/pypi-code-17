#
from objdict import dumps
class Struct:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return self.__class__.__name__ + dumps(self.__dict__)
    def __str__(self):
        return dumps(self.__dict__)

    def __json__(self, data=None, internal=False):
        """ json can be used by derived classes....
        def __json__(self, **kwargs):
            return super().__json__( <mydict>, **kwargs)
        """
        tmp = {'__type__':self.__class__.__name__}
        if data:
            tmp.update(data)
        else:
            tmp.update(self.__dict__)

        if internal:
            return tmp
        return dumps(tmp) #elf.__dict__)

class DictStruct(Struct):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
