from numpy import *
from scipy import *
from scipy.signal import remez, resample
from .halfbandfir import halfbandfir
from fractions import gcd
from .upfirdn import upfirdn


def resample_cascade(x, fs_start, fs_end, N=42):
    """
    Resample a signal from one sampling frequency to another, using a halfband
    filter cascade in the case of drastic resampling ratios, and using polyphase
    implementations whenever possible.  See halfbandfir() for an explanation of
    halfband filters and their application to downsampling, and upfirdn() for an
    explanation of polyphase filtering.

    Parameters
    ----------
    x : 1-D signal array
            The input signal array
    fs_start : int
            The starting sampling frequency
    fs_end : int
            The resultant sampling frequency

    Returns
    -------
    y : 1-D signal array
            The downsampled signal, of length len(x)*(fs_end/fs_start)
    """

    # I'd be very surprised if this is actually ever hit, but let's cover our
    # bases
    fs_start = int(fs_start)
    fs_end = int(fs_end)
    if fs_start == fs_end:
        return x
    fs_start = float(fs_start)
    fs_end = float(fs_end)

    # Generate our halfband fir filter just in case
    h = halfbandfir(N)

    # Let's walk through the filter cascade
    num_steps = int(abs(log2(fs_start / fs_end)))

    # Are we upsampling or downsampling?
    if fs_start < fs_end:
        for step in range(num_steps):
            x = 2 * upfirdn(x, h, uprate=2)[len(h) // 2:-len(h) // 2 + 1]
        fs = fs_start * (2.0**num_steps)
    else:
        for step in range(num_steps):
            x = upfirdn(x, h, downrate=2)[len(h) // 4:-len(h) // 4 + 1]
        fs = fs_start / (2.0**num_steps)

    if fs != fs_end:
        # Now that we're less than a power of two off, we use the typical resample filter
        # to finish off, since this guy works just fine for short filers
        x = resample(x, int(round(fs_end / fs * len(x))))
    return x
