#!/usr/bin/env python

from numpy import *
from scipy import *
from matplotlib.pyplot import *
from utils import *
from libsquiggly.analysis import *
from libsquiggly.util import *
from libsquiggly.resampling import *


def rand_quad(N):
    """
    Return an array of N random numbers belonging to [-1, 1, j, -j]
    """
    return array([random.choice([-1, 1, 1j, -1j]) for idx in range(N)], dtype=complex64)


def do_peak_suppression_test():
    # Our test set of peaks, showing multiple regions of peaks as well as a
    # region that continues right up to the end of the array:
    peaks = [1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 3, 3]
    thresh = 1.5
    found_peaks = collect(suppress_peaks(peaks, thresh))

    if found_peaks != [0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0]:
        print("ERROR: Peak suppression test failture!")
        print(found_peaks)
        return False
    return True


def do_jittered_mfilt_test():
    # Give ourselves a nice spreading sequence
    barker = array([1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1])
    N = 1000

    # Complex, gaussian noise
    jdata = .15 * randn(N) + .15j * randn(N)

    # This stores the subsample jitter we will apply to the barker codes
    jitter = cumsum(.1 * rand(60))

    # This stores the modulation we will apply to the barker codes
    symbols = rand_quad(len(jitter))

    for idx in range(len(jitter)):
        startIdx = 200 + idx * 11
        while jitter[idx] > 1:
            startIdx += 1
            jitter[idx] -= 1
        jdata[startIdx:startIdx + 11] += symbols[idx] * \
            sinc_fractional_shift(barker, jitter[idx])

    # Perform the subsample matched filtering here
    jdata_hat = acollect(subsample_matched_filter(jdata, barker, 5))

    # Recover the symbols by suppressing peaks in jdata_hat
    det_threshold = 0.9
    peaks = acollect(suppress_peaks(jdata_hat, det_threshold))
    recovered_symbols = peaks[nonzero(peaks)]

    if len(symbols) != len(recovered_symbols):
        print("ERROR: Recovered %d symbols when we synthesized %d!" %
              (len(recovered_symbols), len(symbols)))
        print("(Sometimes this happens, which is kind of terrible, but whatever)")
        return False

    f = figure()
    plot(abs(jdata_hat), color='r')
    ylim([0, 1])
    title("Recovered jitterbug")
    savefig("figures/analysis_jitterbug.eps")
    close(f)

    f = figure()
    jdata_plot = scatter(real(jdata_hat), imag(jdata_hat), alpha=0.2)
    recov_plot = scatter(real(recovered_symbols), imag(
        recovered_symbols), color='r', alpha=0.5)
    err = symbols - recovered_symbols
    err_lines = vstack((recovered_symbols, symbols))
    err_plot = plot(real(err_lines), imag(err_lines), color='g', alpha=0.5)
    plot(det_threshold * sin(linspace(0, 2 * pi, 100)), det_threshold *
         cos(linspace(0, 2 * pi, 100)), color='k', alpha=0.3)
    legend(hstack((jdata_plot, recov_plot, err_plot)), [
           "Matched Filter Output", "Detected Symbols", "Error"])
    ylim([-1.1, 1.1])
    xlim([-1.1, 1.1])
    title("Constellation plot of %d decoded de-jittered symbols (avg error: %.3f)" %
          (count_nonzero(recovered_symbols), mean(abs(err))));
    savefig("figures/analysis_consellation.eps")
    close(f)
    return True

from unittest import TestCase
class TestInstantenousFrequencyEstimation(TestCase):
    def test_peak_suppression(self):
        do_peak_suppression_test()

    def test_jittered_mfilt(self):
        do_jittered_mfilt_test()
