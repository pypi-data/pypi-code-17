
"""
def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item

http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
"""



"""
Method              Overloads                   Called for

__init__            Constructor                 Object creation: X = Class( )
__del__             Destructor                  Object reclamation
__add__             Operator +                  X + Y, X += Y
__or__              Operator | (bitwise OR)     X | Y, X |= Y
__repr__,__str__    Printing, conversions       print X, repr(X), str(X)
__call__            Function calls              X( )
__getattr__         Qualification               X.undefined
__setattr__         Attribute assignment        X.any = value
__getitem__         Indexing                    X[key], for loops and other iterations if no _ _iter_ _
__setitem__         Index assignment            X[key] = value
__len__             Length                      len(X), truth tests
__cmp__             Comparison                  X == Y, X < Y
__lt__              Specific comparison         X < Y (or else __cmp__)
__eq__              Specific comparison         X == Y (or else __cmp__)
__radd__            Right-side operator +       Noninstance + X
__iadd__            In-place addition           X += Y (or else __add__)
__iter__            Iteration contexts          for loops, in tests, list comprehensions, map, others
"""




    def _hashify(self, item):
        if not isinstance(item, collections.Hashable):
            return hashify(item)
        else:
            return item

    # TODO recursify
    def hashify(self, items):
        for i, j in enumerate(items):
            if isinstance(i, collections.Iterable):
                items[i] = self.hashify(self._hashify(i))

    # def __repr__(self):
    #     return ''.join(str(i) for i in self)

    # def __repr__(self):
    #      return repr(self)





#http://stackoverflow.com/questions/17020115/how-to-use-setattr-correctly-avoiding-infinite-recursion

