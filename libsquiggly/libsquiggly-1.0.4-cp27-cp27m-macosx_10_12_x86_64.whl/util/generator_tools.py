from numpy import *


def make_gen(x):
    """
    Given sequential data (array, iterator, generator, nditer, etc...) return
    an iterator-compatible version of it.  In practice, this boils down to
    returning x if it already is an iterator, or nditer(x) if it is not.
    """
    import types
    if not isinstance(x, types.GeneratorType) and not isinstance(x, nditer):
        if isinstance(x, ndarray):
            return nditer(x)
        return nditer(array(x))
    return x


def collect(collection):
    """
    Given some kind of iterator called collection, return [x for x in collection]
    """
    return [x for x in collection]


def acollect(collection):
    """
    Given some kind of iterator called collection, return array([x for x in collection])
    """
    return array([x for x in collection])
