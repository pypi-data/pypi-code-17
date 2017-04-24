from numpy import *
from scipy import *
from .talkbox import lpc


def lpc_freq(x, order=2, fs=2.0):
    """
    Analyze a signal using linear predictive coding to discover the linear
    relationships between samples in the signal.  Use this linear model to
    determine dominant frequency components, and return the center frequency of
    that dominant component as the overall frequency of the signal.

    Parameters
    ----------
    x : 1-D signal array
            Preferrably a numpy array
    order : int
            Order of linear model (default 2)
    fs : float
            Sampling rate in Hz (default 2.0)

    Returns
    -------
    freq : float
            The frequency estimatee, according to `fs`
    err : float
            The instantaneous residual error
    """

    # Ask talkbox to do the heavy lifting for us
    A, lpc_error, k = lpc(x, order)

    # Find the roots of the returned polynomial
    R = roots(A)

    # Calculate angle of the strongest peak, convert to Hz
    lpc_freq = angle(R[argmax(abs(R))]) * fs / (2 * pi)
    return lpc_freq, 1.0 / lpc_error


def lpc_freqtrack(x, order=2, win_len=128, step=1, fs=2.0):
    """
    Analyze a signal using linear predictive coding to discover the linear
    relationships between samples in windows of the signal. Use this linear model
    to determine a dominant frequency component, and return the center frequency of
    that dominant component as the instantaneous frequency of the signal across
    time, skipping from window to window according to the `step` parameter.

    Parameters
    ----------
    x : 1-D signal array
            Preferrably a numpy array
    order : int
            Order of linear model (default 2)
    win_len : int
            Length of window over which to build a single model (default 128)
    step : int
            Number of samples to step between windows (default 1)
    fs : float
            Sampling rate in Hz (default 2.0)

    Returns
    -------
    freq : 1-D signal array
            The instantaneous frequency estimates, according to `fs`
    err : 1-D signal array
            The instantaneous residual error
    """

    nlen = int(ceil((len(x) - 1.0 * win_len) / step))

    lpc_estimates = zeros(len(x) // step)
    lpc_error = zeros(len(x) // step)

    # Pad x with zeros
    pad_len = win_len // step
    x = hstack((zeros(pad_len // 2), x, zeros(pad_len // 2)))

    for i in range((len(x) - pad_len) // step):
        window = x[i * step:i * step + win_len]

        lpc_f, lpc_e = lpc_freq(window, order, fs)
        lpc_estimates[i] = lpc_f
        lpc_error[i] = lpc_e

    return lpc_estimates, lpc_error
