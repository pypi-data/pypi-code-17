"""
Useful mathematical functions and objects.
"""

import math as _math
from collections import namedtuple as _namedtuple

_dg = _math.pi / 180


def cos(angle):
    """Cosine of an angle (in degrees)"""
    return _math.cos(angle * _dg)


def sin(angle):
    """Sine of an angle (in degrees)"""
    return _math.sin(angle * _dg)


def tan(angle):
    """Tangent of an angle (in degrees)"""

    return _math.tan(angle * _dg)


class Vec(_namedtuple('Vec', ['x', 'y'])):
    """
    A tuple-based 2D vector.

    Supports all basic arithmetic operations.
    """

    @classmethod
    def from_angle(cls, angle):
        return cls(cos(angle), sin(angle))

    def __new__(cls, x, y=None):
        if y is None:
            x, y = x
        return super(Vec, cls).__new__(cls, x + 0.0, y + 0.0)

    def __repr__(self):
        return '%s(%.1f, %.1f)' % (type(self).__name__, self.x, self.y)

    def __add__(self, other):
        x, y = other
        return Vec(x + self.x, y + self.y)

    def __sub__(self, other):
        x, y = other
        return Vec(self.x - x, self.y - y)

    def __mul__(self, other):
        return Vec(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Vec(self.x / other, self.y / other)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self * (-1) + other

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __abs__(self):
        return _math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self):
        """
        Vector norm.
        """

        return self.__abs__()

    def normalized(self):
        """
        Return unity vector.
        """

        return self / abs(self)

    def perp(self, invert=False):
        """
        Returns a perpendicular vector rotated 90 degrees counter clockwise.
        """

        if invert:
            return Vec(self.y, -self.x)
        return Vec(-self.y, self.x)

    def rotate(self, theta):
        """
        Return rotated vector by the given angle.
        """

        x, y = self
        c, s = cos(theta), sin(theta)
        return Vec(x * c - y * s, x * s + y * c)
