import numpy as _np
from functools import wraps

class Np2dException(Exception):
    """"""

def check_2d(f):
    """Check that the decorated method takes a 2d array"""
    @wraps(f)
    def inner(a, *args, **kwargs):
        if a.ndim != 2:
            raise Np2dException("`a` must be a NumPy array with dim=2")
        return f(a, *args, **kwargs)
    return inner
