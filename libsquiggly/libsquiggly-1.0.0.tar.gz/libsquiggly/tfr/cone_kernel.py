from numpy import *
from scipy import *

# Implements the Generalized Time-Frequency Representation defined in [1]:
# See [2,3] for more background and some exciting applications of mathiness.
#
# [1] Khadra, L., Draidi, J., & Khasawneh, M. (1998). Time-frequency distributions
# based on generalized cone-shaped kernels for the representation of nonstationary
# signals. Journal of the Franklin, 335(5).
#
# [2] Zhao, Y., Atlas, L. E., & Marks, R. J. (1990). The use of cone-shaped kernels
# for generalized time-frequency representations of nonstationary signals. IEEE
# Transactions on Acoustics, Speech, and Signal Processing, 38(7), 1084-1091.
#
# [3] Cohen, L., Generalized phase-space distribution functions. J. Math. Phys.,
# 1966, 7. 781-786

# These are static methods that are used for convenience


def g(tau, beta, p, c, alpha):
    """Generalized window function, use the helpful defines below for quicker coding"""
    return exp(-alpha * abs(tau)**p) / (c * abs(tau)**beta + 1)

# These are the predefined window functions


def ZhaoAtlasWindow(tau, alpha, **kwargs):
    """
    Samples the Zhao-Atlas window for Generalized Cone-Kernel Distributions.
    Pass this function to the GCKD constructor for more control over the distribution.

    Parameters
    ----------
    tau : float (time index)
        Sample the window at this time index

    alpha : float
        Tune the angle of the cone kernel
    """
    return g(tau, beta=1, p=2, c=0, alpha=alpha)


def BornJordanWindow(tau, **kwargs):
    """
    Samples the Born-Jordan window for Generalized Cone-Kernel Distributions.
    Pass this function to the GCKD constructor for more control over the distribution.

    Parameters
    ----------
    tau : float (time index)
        Sample the window at this time index
    """
    return g(tau, beta=1, p=0, c=1, alpha=0)


def MixedWindow(tau, alpha):
    """
    Samples the mixed window for Generalized Cone-Kernel Distributions.
    Pass this function to the GCKD constructor for more control over the distribution.

    Parameters
    ----------
    tau : float (time index)
        Sample the window at this time index
    alpha : float
        Tune the angle of the cone kernel
    """
    return g(tau, beta=1, p=2, c=1, alpha=alpha)


class GCKD:
    """
    Calculate the Generalized Cone-Kernel Distribution of signals, providing superior resolution
    in time and frequency to that of many other time/frequency estimation techniques such as a
    short-time fourier transform or Wigner distribution.

    Construct this object with the desired parameters, then calculate the GCKD with the calculate()
    member function, passing in the desired

    Constructor parameters
    ----------------------
    N : int
        Desired frequency resolution in bins
    g_hat : function
        Pass in a GCKD window function such as `ZhaoAtlasWindow`, or `MixedWindow`
    """

    def __init__(self, N, g_hat=MixedWindow):
        # Initialize static variables that we won't ever change
        self.N = N
        self.M = 2 * N + 1
        self.alpha = -log(.001) / (abs(N)**2)
        self.window = empty((N,))

        # Build up window now
        self.window[0] = 0.5 * g_hat(0, alpha=self.alpha)
        for k in range(1, N):
            self.window[k] = g_hat(k, alpha=self.alpha)

    def y(self, x, L, n, k):
        v0 = n + k + 4 * L
        v1 = n + 4 * L
        a_k = abs(k)
        return vdot(x[v0 - a_k:v0 + a_k], x[v1 - a_k:v1 + a_k])

    def calculate(self, x):
        # Gotta do this padding first
        self.xLen = len(x)
        x = hstack([(4 * self.N) * [0], x, (4 * self.N) * [0]])

        # Copy these out just to save on some typing
        cx = conj(x)
        window = self.window
        y = self.y
        N = self.N
        N_2 = N // 2
        M = self.M

        P = zeros((N_2, self.xLen))
        for n in range(self.xLen):
            P[:, n] = real(fft([(window[k] * y(x, N, n, k))
                                for k in range(N)]))[1:N_2 + 1]
        return 4 * array(P)


# Given a signal x and a frequency resolution parameter NFFT, calculate the
# generalized cone kernel distribution of x across every time point and
# frequency
def gckd(x, NFFT):
    """
    Convenience method when all you really want to do is crunch through some data.
    Uses `MixedWindow` by default.  Crank up N for a good time, and a warm CPU.

    Parameters
    ----------
    x : 1-D signal array
        Preferrably a numpy array
    N : int
        Desired frequency resolution in bins.
    """
    return GCKD(NFFT, MixedWindow).calculate(x)
