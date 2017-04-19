from numpy import *


def clamp(x, minval, maxval):
    """
    Given input x, ensure values do not exceed the range [minval, maxval]
    """
    return min(max(x, minval), maxval)


class RollingBuffer(object):
    """
    Holds a buffer of the last N samples, with a given dtype. Access to the
    buffer is given through `buff`, append items via `push()`
    """

    def __init__(self, N, dtype=float32):
        self.buff = zeros(N, dtype=dtype)

    def push(self, data):
        # If we can iterate over data, do it!  Otherwise, fail out:
        try:
            for x in data:
                self.push(x)
        except TypeError:
            self.buff = roll(self.buff, -1)
            self.buff[-1] = data
