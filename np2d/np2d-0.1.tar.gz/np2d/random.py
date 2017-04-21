from .base import *
import numpy as _np

@check_2d
def choice2d(a, size=None, replace=True, p=None):
    """Choose random samples from a 2-D array.

    Parameters
    ----------
    a : array
        2-D array to sample
    size : int
        Number of elements to choose from array
    replace : bool
        Sample with replacement
    p : 2-D array
        Array of weights for each element in the array.

    Returns
    -------
    samples : 1-D array
        The generated random samples
    indices :
    """
    arr = _np.ravel(a)
    if p is not None:
        parr = _np.ravel(p)
    else:
        parr = None
    # Build an index array
    index_arr = _np.arange(len(arr))
    # Sample from indices array
    sample_indices = _np.random.choice(index_arr, size=size, replace=replace, p=parr)
    # Put the indices back in original
    row, col = _np.unravel_index(sample_indices, dims=a.shape)
    samples = arr[sample_indices]
    indices = _np.column_stack((row, col))
    return samples, indices
