from numpy import *
from scipy import *
from scipy.signal import remez, firwin2


def halfbandfir(N):
    """
    Generate a halfband filter as an efficient, correct multirate downsampling filter.

    Given a half-length N, generate a filter with cutoff .5 and coefficients such that
    every other coefficient is (nearly) equal to zero.  This property is desirable
    for anti-aliasing filters so as to ensure that energy above fs/4 is minimized

    Parameters
    ----------
    N : int
        A half-length parameter, must conform to the set [2, 6, 10, ... n, n+4, ...]

    Returns
    -------
    h : 1-D signal array
        An FIR filter for use with methods such as upfirdn().  Note that the length
        is not actually N, it will be 2*(N+1)
    """

    if N < 2:
        raise ValueError("N cannot be less than 2!")

    R = (N - 2) / 4
    if R * 4 + 2 != N:
        raise ValueError("N must conform to (i + 2)*4, where i is an integer!")

    # Create filter with symmetric regions about fs/4
    #h = remez(N+1, bands=[0, 0.48, 0.52, 1], desired=[1, 0], weight=[1,1], Hz=2)
    h = firwin2(N + 1, freq=[0, 0.48, 0.52, 1],
                gain=[1, 1, 0, 0], window=("kaiser", 10))

    # Force down the impulse response to zero on every other sample
    h[1::2] = 0

    # This is mucho importanto!
    h[N // 2] = .5

    # Auto-convolve to get zero phase response :P
    return convolve(h, h)
