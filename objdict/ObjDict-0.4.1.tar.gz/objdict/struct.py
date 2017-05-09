#
from objdict import dumps
class Struct:
    def __init__(self, *args, **kwargs):
        keystxt = kwargs.get('__keys__', getattr(self,'__keys__', '*'))
        keys = keystxt.split()
        aster = '*' in  keys
        if aster:
            keys.remove('*')
        keyset = set(keys)
            
        if len(args)> len(keys):
            raise TypeError("{} has maxium {} list arguments".format(
                    self.__class__.__name__, len(args))
                )
        for key, val in zip(keys, args):
            setattr(self, key, val)
        shortage = len(keys) - len(args)
        if shortage:
            for key in keys[-shortage:]:
                if key not in kwargs:
                    raise TypeError("{} has missing arg {} ".format(
                        self.__class__.__name__, key)
                                   )

        for key, val in kwargs.items():
            if not aster and not key in keyset:
                raise TypeError("{} has no {} argument".format(
                    self.__class__.__name__, len(keys))
                               )
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
            tmp.update({k:v for k, v in self.__dict__.items() if k[0]!= '_'})

        if internal:
            return tmp
        return dumps(tmp) #elf.__dict__)

class DictStruct(Struct):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
