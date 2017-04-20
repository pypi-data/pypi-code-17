from numpy import *
from scipy import *

# This function is so awesome, I just have to give him his own file


def max_peak(P, fs=2.0):
    """
    The simplest instantaneous-frequency tracking algorithm around.  Simply plug in
    your time/frequency representation along with your sampling rate and this will
    find the peak in frequency for each timepoint.  Combine with something like
    `guided_peaktracing` for more reasonable results.

    Parameters
    ----------
    P : 2-D array
            The time/frequency representation to be analyzed
    fs : float
            The sampling rate (in Hz) of the signal (default 2.0)
    """
    peak_bins = argmax(abs(P), axis=0)

    # Convert to hertz
    return peak_bins * fs / (2 * P.shape[0])
