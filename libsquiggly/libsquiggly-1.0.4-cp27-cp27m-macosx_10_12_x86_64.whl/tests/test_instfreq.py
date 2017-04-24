#!/usr/bin/env python
from __future__ import print_function

from numpy import *
from scipy import *
from matplotlib.pyplot import *
from utils import *
from libsquiggly.util import *
from libsquiggly.instfreq import *
from libsquiggly.tfr import *


# Generic test harness for our instantaneous-frequency estimation code
def do_instfreq_test(x, f_gt, sig_name):
    # Setup spectrogram parameters.  Note that we use spectrogram to calculate
    # the STFT for TFR-based estimation methods such as max_peak and
    # peaktracing
    NFFT = 256
    N = len(x)
    fs = 2.0
    t = linspace(0, N / fs, N)

    # Always plot into a new figure
    f = figure()
    P = spectrogram(x, NFFT=NFFT, noverlap=NFFT - 1, fs=fs, cbar=False)

    # Calculate frequency tracks.  Note that TFR-based estimation methods such as
    # max_peak and anything with peaktracing in the name are indexed in time by
    # STFT time bins.  In this case, noverlap = NFFT-1, therefore the time bins
    # are just samples, but in general you won't have such densely overlapped bins
    # in time, and thus you will need to calculate a proper time base.
    f_maxpeak = max_peak(P, fs)
    f_lsharm = lsharm_freqtrack(x, freqs=linspace(0.1, 1, 200), weights=[
                                1, .5, .5, .5, .5], fs=fs, skip=10)
    f_guided = guided_peaktracing(P, guide=f_maxpeak, sigma=15.0, fs=fs)
    f_windowed = windowed_peaktracing(P, sigma=15.0, fs=fs)
    f_lpc, lpc_error = lpc_freqtrack(x, order=2, fs=fs)

    # Plot everything over the spectrogram
    plot(t, f_gt)
    plot(t, f_lsharm)
    plot(t, f_maxpeak)
    plot(t, f_guided)
    plot(t, f_windowed)
    plot(t, f_lpc)

    # Make it look all "professional"
    title("Spectrogram of " + sig_name)
    xlabel("Samples")
    ylabel("Frequency (normalized)")
    legend(["Ground truth", "least-squares harmonic", "max_peak",
            "guided_peaktracing", "windowed_peaktracing", "lpc"])
    savefig("figures/instfreq_" + sig_name + ".eps")
    close(f)


from unittest import TestCase
class TestInstantenousFrequencyEstimation(TestCase):
    def test_sin(self, N=8192):
        x_fm, f_fm = gen_fm_track(N, f0=.5, df=.35)
        do_instfreq_test(x_fm, f_fm, "frequency-modulated sinusoid")

    def test_hamonic(self, N=8192):
        x_harm, f_harm = gen_harmonic_track(N, K=5, f0=.15, df=.05)
        do_instfreq_test(x_harm, f_harm,"harmonic frequency-modulated sinusoid")

    def test_hopping(self, N=8192):
        x_hopping, f_hopping = gen_hopping_track(N, 7, fmin=.2, fmax=.8)
        do_instfreq_test(x_hopping, f_hopping, "frequency-hopping sinusoid")

    def test_wideband(self, N=8192):
        x_wide, f_wide = gen_wideband_track(N, width=.1, f0=.5, df=.15)
        do_instfreq_test(x_wide, f_wide, "wideband nonstationary signal")
