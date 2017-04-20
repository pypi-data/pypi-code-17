from numpy import *
from scipy import *
from scipy.signal import *


def lsharm_freqtrack(x, freqs=None, weights=[1, .5, .5], fs=2.0, win_len=100, skip=1):
    """
    Anaylze a signal using least-harmonic squares analysis [1] returning the
    dominant fundamental frequency component found. This analysis is done by
    "guessing" fundamental frequencies (given in `freqs`) and then summing up
    spectral energy contained in the fundamental frequency and `len(weights)`
    integer multiples of that fundamental frequency.  Spectral energy is
    calculated about each timepoint by applying Goertzel filters to the
    neighborhood of the time instant under scrutiny. The length of signal
    analyzed for frequency content is governed by `win_len`.

    Parameters
    ----------
    x : 1-D signal array
            The data to be analyzed
    freqs : 1-D float array
            Array of fundamental frequencies to search over, in Hz. Default
            is to search over `linspace( .5*fs/len(weights), fs/len(weights), 100)`
    weights : 1-D float array
            The weighting factor to give each harmonic found in the signal, simultaneously
            controls how many harmonics to take into account (default [1, 0.5, 0.5])
    fs : float
            Sampling rate in Hz (default 2.0)
    win_len : int
            The window length over which the Goertzel filter will be applied.  Minimum
            value is 3, defaults to 100
    skip : int
            The number of samples to skip the analysis window forward by.  The
            resulting frequency track will be upsampled after calculation to yield
            a frequency track of equal length to `x`

    Returns
    -------
    freq : 1-D signal array
            The instantaneous frequency estimates, according to `fs`

    References
    ----------
    [1] Qin Li; Atlas, L., "Time-variant least squares harmonic modeling,"
    Acoustics, Speech, and Signal Processing, 2003. Proceedings. (ICASSP '03)
    """

    if freqs is None:
        freqs = linspace(.5 * fs / len(weights), fs / len(weights), 100)

    # Build Goertzel filterbanks, excluding any filters that exceed nyquist
    fundamental_filters = {}
    for f0 in freqs:
        filterbank = []
        max_order = min(len(weights), int(fs / (2 * f0)))
        for k in range(max_order):
            b = weights[k] * array([1, -exp(-2j * pi * (k + 1) * f0 / fs)])
            a = weights[k] * \
                array([1, -2 * cos(2 * pi * (k + 1) * f0 / fs), 1])
            filterbank += [(b, a)]
        fundamental_filters[f0] = filterbank

    # Zero-pad x so that we can actually perform the Goertzel-filtering at
    # every point
    datalen = len(x)
    x = hstack((zeros(win_len // 2), x, zeros(win_len // 2)))
    lsharm_estimate = zeros(datalen // skip)

    for idx in range(datalen // skip):
        # Grab the window of data centered about x[idx] in the original
        # non-padded signal
        window = x[idx * skip:idx * skip + win_len]

        # Calculate total power of each fundamental frequency, as well as error
        P = zeros(len(freqs))

        # For each fundamental frequency, apply Goertzel filters to data:
        for f_idx in range(len(freqs)):
            f0 = freqs[f_idx]
            filterbank = fundamental_filters[f0]
            C = zeros(len(filterbank), dtype=complex)

            for k in range(len(filterbank)):
                # Filter with Goertzel filter
                temp = lfilter(filterbank[k][0], filterbank[k][1], window)

                # Phase-correct last element of Goertzel filter and square it
                # away in C
                C[k] = exp(-2j * pi * (k + 1) * f0 / fs *
                           (win_len - 1)) * temp[-1] / sqrt(win_len)

            # Store total power of this fundamental frequency
            P[f_idx] = sqrt(real(vdot(C, C)))

        # Save highest frequency estimate into lsharm_estimage
        lsharm_estimate[idx] = freqs[argmax(P)]

    # Return the goods, after upsampling them
    return resample(lsharm_estimate, datalen)
