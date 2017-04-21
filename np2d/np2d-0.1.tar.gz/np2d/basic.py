import numpy as _np
from .base import *

@check_2d
def kmax(a, k):
    """Return the (row, col) indices of the n largest arguments in the 2d array.

    Parameters
    ----------
    a : array
        2d numpy array
    k : int
        number of arguments to select.

    Returns
    -------
    el : 1-D array
        k max arguments.
    indices : 2-D array.
        2-D array of indices. Column 0 is first index, column 2 is second index.
    """
    n, m = a.shape
    vec = a.flatten()
    vec_ = vec.argsort()[::-1]
    top_vec = vec_[:k]
    row = top_vec // n
    col = top_vec % n
    indices = _np.column_stack((row, col))
    return a[row, col], indices

@check_2d
def kmin(a, k):
    """Return the (row, col) indices of the n largest arguments in the 2d array.

    Parameters
    ----------
    a : array
        2d numpy array
    k : int
        number of arguments to select.

    Returns
    -------
    el : 1-D array
        k min arguments.
    indices : 2-D array.
        2-D array of indices. Column 0 is first index, column 2 is second index.
    """
    n, m = a.shape
    vec = a.flatten()
    vec_ = vec.argsort()
    top_vec = vec_[:k]
    row = top_vec // n
    col = top_vec % n
    indices = _np.column_stack((row, col))
    return a[row, col], indices
