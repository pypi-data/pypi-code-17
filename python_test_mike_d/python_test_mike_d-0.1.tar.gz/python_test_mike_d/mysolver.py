import numpy as np
from enum import Enum
import runner
from math import log


class ComplexityError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Complexity():

    constant = 1
    linear = 2
    linear_logarithmic = 3
    square = 4
    cubic = 5

    def __init__(self,value):
        self.complexity = value

    def to_string(self):
        if self.complexity == Complexity.constant:
            return "O(c)"
        if self.complexity == Complexity.linear:
            return "O(n)"
        if self.complexity == Complexity.linear_logarithmic:
            return "O(n * log(n))"
        if self.complexity == Complexity.square:
            return "O(n^2)"
        if self.complexity == Complexity.cubic:
            return "O(n^3)"
        else:
            raise ComplexityError("to_string error - can't match 'if' cases")


def fit_constant(x, y):
    return np.array([y[0]])


def fit_linear(x, y):
    return np.polyfit(x, y, 1)


def fit_square(x, y):
    return np.polyfit(x, y, 2)


def fit_cubic(x, y):
    return np.polyfit(x, y, 3)


def fit_function(complexity, x, y):

    poly_fitters = {
        Complexity.constant: fit_constant,
        Complexity.linear: fit_linear,
        Complexity.linear_logarithmic: fit_square,
        Complexity.square: fit_square,
        Complexity.cubic: fit_cubic
    }
    try:
        return poly_fitters[complexity.complexity](x, y)
    except KeyError:
        raise ComplexityError("fit_function error - no key for pseudo-switch dictionary")


def get_coefficient(y):
    coefficients = []
    for i in range(y.size - 1):
        coefficient = y[i+1]/y[i]
        coefficients.append(coefficient)
    coefficients = np.array(coefficients)
    return coefficients.max()


def estimate_complexity(coefficient):
    n = runner.STEP
    complexity = Complexity(Complexity.constant)
    if coefficient >= n:
        complexity = Complexity(Complexity.linear)
    if coefficient >= n * log(n):
        complexity = Complexity(Complexity.linear_logarithmic)
    if coefficient >= n * n:
        complexity = Complexity(Complexity.square)
    if coefficient >= n * n * n:
        complexity = Complexity(Complexity.cubic)
    return complexity


def wrap_time_function(poly_values):
    def wrapper(n):
        return np.polyval(poly_values, n)
    return wrapper


def wrap_size_function(poly_values):
    def wrapper(target):
        b = 10
        while np.polyval(poly_values, b) < target:
            b *= 10
        a = 1
        while a <= b:
            mid = (a+b)/2
            if np.polyval(poly_values, mid) < target:
                a = mid+1
            else:
                b = mid-1
        return int(a)
    return wrapper


def solve(measures):
    measures = np.array(measures)

    x = measures[:, 0]
    y = measures[:, 1]

    coefficient = get_coefficient(y)
    complexity = estimate_complexity(coefficient)
    complexity_class = complexity.to_string()
    print("Estimated complexity class of the algorithm is " + complexity_class)
    poly_values = fit_function(complexity, x, y)

    time_function = wrap_time_function(poly_values)
    size_function = wrap_size_function(poly_values)

    return time_function, size_function
