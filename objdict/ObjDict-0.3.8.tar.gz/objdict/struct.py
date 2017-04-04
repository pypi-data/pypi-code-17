#
from objdict import dumps
class Struct:
    def __repr__(self):
        return self.__class__.__name__ + dumps(self.__dict__)
    def __str__(self):
        return dumps(self.__dict__)

    def __json__(self, internal=False):
        tmp = {'__type__':self.__class__.__name__}
        tmp.update(self.__dict__)
        if internal:
            return tmp
        return dumps(tmp) #elf.__dict__)

class DictStruct(Struct):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
