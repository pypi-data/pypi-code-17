#!/usr/bin/env python

from numpy import *
from scipy import *
from scipy.signal import *
from matplotlib.pyplot import *
from libsquiggly.util import *
from libsquiggly.resampling import *
from libsquiggly.resampling.upfirdn import upfirdn


def do_resampling_test(fs_start, fs_end, N=42):
    t_start = arange(fs_start) * 1.0 / fs_start
    t_end = arange(fs_end) * 1.0 / fs_end

    # Generate a super-super-super oversampled sinusoid
    x_sin = sin(2 * pi * 10.0 * t_start)
    y_sin = resample_cascade(x_sin, fs_start, fs_end, N=N)
    z_sin = resample(x_sin, fs_end)
    f = figure()
    plot(t_start, x_sin)
    plot(t_end, y_sin)
    plot(t_end, z_sin)
    xlabel("Time (s)")
    ylabel("Amplitude")
    title("Sinusoidal signal (%.2fHz -> %.2fHz)" % (fs_start, fs_end))
    legend(["Original", "Cascaded", "Classical"])
    savefig("figures/resampling_sin_%.2f_%.2f.eps"%(fs_start, fs_end))
    close(f)

    # Now try square wave
    x_sqr = acollect(map(lambda t: int(t * 8) % 2, t_start))
    y_sqr = resample_cascade(x_sqr, fs_start, fs_end, N=N)
    z_sqr = resample(x_sqr, fs_end)
    f = figure()
    plot(t_start, x_sqr)
    plot(t_end, y_sqr)
    plot(t_end, z_sqr)
    xlabel("Time (s)")
    ylabel("Amplitude")
    title("Square-wave signal (%.2fHz -> %.2fHz)" % (fs_start, fs_end))
    legend(["Original", "Cascaded", "Classical"])
    savefig("figures/resampling_square_%.2f_%.2f.eps"%(fs_start, fs_end))
    close(f)

    # Now sawtooth wave!
    x_tri = sawtooth(8 * 2 * pi * t_start)
    y_tri = resample_cascade(x_tri, fs_start, fs_end, N=N)
    z_tri = resample(x_tri, fs_end)
    f = figure()
    plot(t_start, x_tri)
    plot(t_end, y_tri)
    plot(t_end, z_tri)
    xlabel("Time (s)")
    ylabel("Amplitude")
    title("Sawtooth signal (%.2fHz -> %.2fHz)" % (fs_start, fs_end))
    legend(["Original", "Cascaded", "Classical"])
    savefig("figures/resampling_sawtooth_%.2f_%.2f.eps"%(fs_start, fs_end))
    close(f)


from unittest import TestCase
class TestResampling(TestCase):
    def test_resampling_8192_128(self):
        do_resampling_test(8192, 128)

    def test_resampling_128_8192(self):
        do_resampling_test(128, 8192)

    def test_resampling_8192_100(self):
        do_resampling_test(8192, 100)

    def test_resampling_100_8192(self):
        do_resampling_test(100, 8192)
