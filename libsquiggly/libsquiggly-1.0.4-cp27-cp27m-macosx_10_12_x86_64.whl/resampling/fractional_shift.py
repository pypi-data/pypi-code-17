from numpy import *
from scipy import *


def linear_fractional_shift(x, shift):
    """
    Linearly resample a signal, shifted by a fractional sample period

    Parameters
    ----------
    x : 1-D signal array
        The signal to shift
    shift : number within [0, 1]
        The fraction of a sample period to shift the signal

    Return values
    -------------
    y : 1-D signal array
        The shifted signal
    """
    return convolve(x, array([1 - shift, shift]))[:-1]


def sinc_fractional_shift(x, shift=0.5):
    """
    Sinc resample a signal, shifted by a fractional sample period

    Parameters
    ----------
    x : 1-D signal array
        The signal to shift
    shift : number within [0, 1]
        The fraction of a sample period to shift the signal

    Return values
    -------------
    y : 1-D signal array
        The shifted signal
    """
    N = len(x)
    f = hstack((arange((N + 1) // 2), -arange(N // 2, 0, -1)))
    z = exp(-2j * pi * shift * f / N)
    if N % 2 == 0:
        z[N // 2] = real(z[N // 2])
    return real(ifft(fft(x) * z))
