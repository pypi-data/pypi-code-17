#!/usr/bin/env python

from numpy import *
from scipy import *
from matplotlib.pyplot import *
from utils import *
from libsquiggly.util import *
from libsquiggly.tfr import *

# Generic test harness for our instantaneous-frequency estimation code
def do_tfr_test(x, f, sig_name):
    # Setup spectrogram parameters.
    NFFT = 512
    N = len(x)
    fs = 2.0
    t = linspace(0, N / fs, N)

    # Plot the spectrogram
    f = figure()
    P_stft = spectrogram(x, NFFT=NFFT, noverlap=NFFT - 1, fs=fs, cbar=False)
    #plot(t, f)
    title("Spectrogram of " + sig_name)
    xlabel("Samples")
    ylabel("Frequency (normalized)")
    savefig("figures/tfr_spectrogram_" + sig_name + ".eps")
    close(f)

    # Plot the GCKD
    f = figure()
    P_gckd = gckdgram(x, NFFT=NFFT, fs=fs, cbar=False)
    #plot(t, f)
    title("GCKD-gram of " + sig_name)
    xlabel("Samples")
    ylabel("Frequency (normalized)")
    savefig("figures/tfr_gckd_" + sig_name + ".eps")
    close(f)


from unittest import TestCase
class TestTimeFrequencyRepresentations(TestCase):
    def test_fm_sinusoid(self, N=8196):
        x_fm, f_fm = gen_fm_track(N, f0=.5, df=.35)
        do_tfr_test(x_fm, f_fm, "frequency-modulated sinusoid")

    def test_hopping_sinusoid(self, N=8196):
        x_hopping, f_hopping = gen_hopping_track(N, 7, fmin=.001, fmax=.8)
        do_tfr_test(x_hopping, f_hopping, "frequency-hopping sinusoid")

    def test_wideband_track(self, N=8196):
        x_wideband, f_wideband = gen_wideband_track(N, width=.1, f0=.5, df=.15)
        do_tfr_test(x_wideband, f_wideband, "wideband nonstationary signal")
