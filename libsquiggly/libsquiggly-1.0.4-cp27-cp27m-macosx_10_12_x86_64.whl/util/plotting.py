from numpy import *
from scipy import *
from scipy.signal import *
from matplotlib.pyplot import *
from ..tfr import gckd, stft
import sys
#ion()


def imagesc(x, xstart=0, xlim=1, ystart=0, ylim=1, cbar=True):
    """
    Plot a 2-D array normalized with no interpolation, on the given axis ranges.

    Parameters
    ----------
    x : 2-D signal array
        Preferrably a numpy array
    {x,y}start : float
        The starting point for the {x,y} axis
    {x,y}lim : float
        The ending point for the {x,y} axis
    cbar : boolean
        Whether or not to show a colorbar (default True)
    """
    xf = x.flatten()
    mini = abs(min(xf[isfinite(xf)]))
    maxi = abs(max(xf[isfinite(xf)]))
    clf()
    imshow((x - mini) / (maxi - mini), extent=(xstart, xstart + xlim, ystart,
                                               ystart + ylim), origin='lower', interpolation='nearest', cmap=cm.bone)
    axis('tight')
    if cbar:
        colorbar()
    draw()


def spectrogram(x, NFFT=256, fs=2.0, noverlap=128, windowfunc=hann, zeropadding="sandwich", cbar=True):
    """
    Plot the STFT of a signal using stft() and imagesc()

    See stft() and imagesc() for their respective parameter meanings
    """
    P = stft(x, NFFT, fs, noverlap, windowfunc, zeropadding)
    imagesc(abs(P), xlim=len(x) / fs, ylim=fs / 2, cbar=cbar)
    return P


def gckdgram(x, NFFT=256, fs=2.0, cbar=True):
    """
    Plot the GCKD of a signal using gckd() and imagesc()

    See gckd() and imagesc() for their respective parameter meanings
    """
    P = gckd(x, NFFT)
    imagesc(abs(P), xlim=len(x) / fs, ylim=fs / 2, cbar=cbar)
    return P


def pause():
    # Flush stdin first, so that we don't have to worry about the user
    # pressing something in the past
    try:
        # On sane operating systems, use tcflush()
        from termios import tcflush, TCIFLUSH
        tcflush(sys.stdin, TCIFLUSH)
    except ImportError:
        # On windows, use msvcrt
        from msvcrt import kbhit, getch
        while kbhit():
            getch()

    # If we're running using the MacOSX backend, just manually do the show()
    # here
    show(block=False)
    try:
        raw_input("Press any key to continue...")
    except NameError:
        input("Press any key to continue...")
