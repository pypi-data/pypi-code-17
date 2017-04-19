from numpy import *
from scipy import *
from scipy.signal import *


def gen_fm_track(N, f0, df):
    """
    Generate a Frequency-Modulated sinusoid in the presence of noise, to test
    instantaneous-frequency tracking code

    Parameters
    ----------
    N : int
            Number of samples to generate
    f0 : float
            Center frequency of sinusoid to generate (in normalized frequency)
    df : float
            Spread of frequency to FM the sinusoid, must be less than `f0`
    """
    # Generate FM'ed sinusoid
    f = f0 + df * sin(arange(N) * 2 * pi / N)
    x = sin(arange(N) * pi * f0 - N / 2 * df * cos(arange(N) * 2 * pi / N))

    # Return x in the presence of background noise, as well as the "ground
    # truth" frequency track
    return x + 0.1 * randn(N), f


def gen_harmonic_track(N, K, f0, df):
    """
    Generate a harmonic series of Frequency-Modulated sinusoids in the presence
    of noise, to test instantaneous-frequency tracking code

    Note that K*(f0 + df) must be less than 1, otherwise aliasing may occur

    Parameters
    ----------
    N : int
            Number of samples to generate
    K : int
            Number of harmonics to generate
    f0 : float
            Center frequency of fundamental frequency (in normalized frequency)
    df : float
            Spread of frequency to FM the fundamental frequency, must be less than `f0`
    """
    # Generate FM'ed frequency tracks
    x = zeros(N)
    f = f0 + df * sin(arange(N) * 2 * pi / N)
    for k in arange(1, K + 1):
        x += sin(arange(N) * pi * f0 * k - N / 2 * df *
                 cos(arange(N) * 2 * pi / N) * k) * 1.05**k

    # Return x in the presence of background noise, as well as the "ground
    # truth" frequency track
    return x + 0.1 * randn(N), f


def gen_hopping_track(N, num_freqs, fmin=0.2, fmax=0.6):
    """
    Generate a frequency-hopping sinusoid in the presence of noise, to test
    instantaneous-frequency tracking code

    Parameters
    ----------
    N : int
            Number of samples to generate
    num_freqs : int
            Number of separate frequencies to generate
    fmin : float
            Lower bound on random frequencies to generate (default 0.2)
    fmax : float
            Upper bound on random frequencies to generate (default 0.8)
    """

    # Generate random frequencies
    freqs = (fmax - fmin) * rand(num_freqs) + fmin

    x = zeros((N,))
    n_len = N // num_freqs

    # Generate sinusoids for each frequency
    start_phase = 0
    for idx in range(num_freqs):
        # Generate a sinusoid of the current frequency, save it out to x
        x[idx * n_len:(idx + 1) * n_len] = sin(pi *
                                               arange(n_len) * freqs[idx] + start_phase)

        # Track phase to avoid discontinuities
        start_phase = (pi * n_len * freqs[idx] + start_phase) % (2 * pi)

    # Get our ground-truth frequencies
    f = array([[f for z in range(n_len)] for f in freqs]).flatten()

    # If N%num_freqs != 0, we need to fill up the last few samples!
    if N % num_freqs != 0:
        x[-(N % num_freqs):] = sin(2 * pi * arange(N %
                                                   num_freqs) * freqs[-1] + start_phase)
        f = append(f, array([freqs[-1]] * (N % num_freqs)))

    return x, f


def gen_wideband_track(N, f0, width, df):
    """
    Generate a nonstationary wideband process in the presence of noise

    Parameters
    ----------
    N : int
            Number of samples to generate
    f0 : float
            Center frequency of wideband process to generate (in normalized frequency)
    width : float
            Width of wideband process to generate (in normalized frequency)
    df : float
            Spread of frequency to FM the process, must be less than `f0`
    """
    # Generate FM'ed sinusoid
    f = f0 + df * sin(arange(N) * 2 * pi / N)
    carrier = sin(arange(N) * pi * f0 - N / 2 *
                  df * cos(arange(N) * 2 * pi / N))

    # Generate wideband process by filtering noise to desired width
    b, a = butter(2, width)
    modulator = lfilter(b, a, randn(N))

    # Modulator wideband process up onto frequency track, then return that in the
    # presence of noise, as well as the "ground truth" frequency track
    return carrier * modulator + 0.001 * randn(N), f
