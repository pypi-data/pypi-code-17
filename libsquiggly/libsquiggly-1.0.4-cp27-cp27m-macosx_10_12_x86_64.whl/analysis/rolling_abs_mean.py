from numpy import *
from ..util import RollingBuffer, make_gen


def rolling_abs_mean(data, N, mode="same"):
    """
    Calculate the mean of the absolute value of a sliding window of length N

    Parameters
    ----------
    data : 1-D signal (array or iterator)
    The actual timeseries to operate on.  This should be an iterator, so
    if you have a numpy array called x, pass in nditer(x) to this function
    N : integer
            The length of the sliding window, in samples
    mode : string
    Similar to numpy.convolve(); output length should be "same" or "valid" to disable/enable
    chomping of output that is due to transient response at the beginning/end of a stream.
    Note that since this function assumes an infinite stream, it only bothers with the beginning

    Yielded values
    --------------
    mean : float
            The mean of the window at its current shift in the data stream
    """
    data = make_gen(data)

    rb = RollingBuffer(N, dtype=float64)
    # Pre-load so that we're operating in "valid" mode
    for idx in range(N - 1):
        rb.push(abs(next(data)))

    # Now, give them the mean!
    for x in data:
        rb.push(abs(x))
        yield mean(rb.buff)
