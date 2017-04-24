from numpy import *
from scipy import *

# Precalculate X inverse for the x coordinates [-1, 0, 1]
# We disregard the last row, since we don't care about c
X_inv = .5 * array([
    [1, -2, 1],
    [-1, 0, 1],
    #[0, 2, 0]
])


def quadratic_peak_interpolation(P_slice):
    """
    Given a discrete PSD estimate, do quadratic interpolation between the peak and
    the two neighboring data points to get sub-bin resolution

    Parameters
    ----------
    P_slice : 1-D array
            The discrete PSD estimate
    """
    # Get the peak index
    peak_idx = min(max(argmax(P_slice), 1), len(P_slice) - 2)

    # Now perform quadratic interpolation to get sub-bin accuracy (we assume
    # the peak is never the first or last index)
    Z = dot(X_inv, P_slice[peak_idx - 1:peak_idx + 2])

    # We now have the a and b coefficients of the parabola (we disregard c), so we find peak offset
    # and use that to get sub-bin accuracy:
    return peak_idx - Z[1] / (2 * Z[0])


def windowed_peaktracing(P, sigma=5.0, fs=2):
    """
    Given a time/frequency representation `P`, find the maximum point in time and
    frequency then work out from that point, finding peaks in frequency spectrum
    that do not deviate significantly from previously found peaks.

    Parameters
    ----------
    P : 2-D array
            The time/frequency representation to be traced through
    sigma : float
            Tuning parameter on how stricly the guide should be followed (default 5.0)
    fs : float
            The sampling rate (in Hz) of the signal (default 2.0)
    """
    max_idx = unravel_index(argmax(P), P.shape)

    # Step forward and backward
    peak_f = zeros((P.shape[1],))
    peak_f[max_idx[1]] = max_idx[0]
    for t in range(max_idx[1] + 1, P.shape[1]):
        # Build an appropriate window centered on peak_f[t-1]
        window = exp(-(peak_f[t - 1] - arange(P.shape[0]))**2 / sigma**2)

        peak_f[t] = quadratic_peak_interpolation(P[:, t] * window)

    for t in range(max_idx[1] - 1, 0, -1):
        # Build an appropriate window centered on peak_f[t+1]
        window = exp(-(peak_f[t + 1] - arange(P.shape[0]))**2 / sigma**2)

        peak_f[t] = quadratic_peak_interpolation(P[:, t] * window)

    return peak_f * fs / (2 * P.shape[0])


def guided_peaktracing(P, guide, sigma=5.0, fs=2.0):
    """
    Given a time/frequency representation `P`, and a rough estimate `guide`,
    trace peaks throughout the signal that are close to the guide

    Parameters
    ----------
    P : 2-D array
            The time/frequency representation to be traced through
    guide : 1-D array
            For each time index in P, a frequency estimate (in bins)
    sigma : float
            Tuning parameter on how stricly the guide should be followed (default 5.0)
    fs : float
            The sampling rate (in Hz) of the signal (default 2.0)
    """
    peak_f = zeros((P.shape[1],))
    for t in range(P.shape[1]):
        guide_idx = guide[t] * 2 * P.shape[0] / fs
        # Build an appropriate window centered on peak_f[t+1]
        window = exp(-(guide_idx - arange(P.shape[0]))**2 / sigma**2)

        peak_f[t] = quadratic_peak_interpolation(P[:, t] * window)

    return peak_f * fs / (2 * P.shape[0])
