#!/usr/bin/env python3
"""Library for mathematical operations

"""


import math
import numpy as np


class Solver(object):
    """ Solver class with mathematical operations


    """

    def __init__(self):
        """ Initialization of `Solver`

        Initialization of basic variables and preparing dictionaries
        for eval.
        """
        # Variables
        self.ans = 0
        """float: Result of last operation"""
        self.variables = {}
        """dict: Dictionary with variables"""
        self.variables['ans'] = self.ans

        # Constants
        self.constants = {'pi': math.pi, 'e': math.e}
        """dict: Dictionary with constants pi and e"""
        self.__make_dicts()
        self.is_degree = False
        """bool: Indicates if trigonometric are set to operate with radians
        or degrees"""

    def switch_rad_deg(self):
        """Method for switching between radians and degrees

        Method sets `self.is_degree` parameter to True or False
        """
        self.is_degree = not self.is_degree

    def solve(self, text):
        """Method for solving mathematical expression from string

        Method solves mathematical expresion and returns result or string with
        error
        Args:
            param1 (str): String with expression
        Returns:
            Result or error string
        """
        try:
            self.ans = eval(text, {}, {**self.variables,
                                       **self.constants,
                                       **self.functions,
                                       **self.trigon,
                                       **self.atrigon,
                                       'ans': self.ans})
            return self.ans

        except ZeroDivisionError:
            return "Division by zero!"
        except ValueError:
            return "Values out of range (asin, log..)"
        except Exception as e:
            return "Invalid syntax"

    @staticmethod
    def std(x):
        """Method for standard deviation

        Method counts standard deviation from array of numbers
        Args:
            param1 (list): List of numbers
        Returns:
            Standard deviation
        """
        return math.sqrt(1 / (len(x) - 1) *
                         (sum([a**2 for a in x]) - sum(x)**2/len(x)))

    @staticmethod
    def __switch(sw, function):
        """Switch between radians and degrees"""
        def degree_wrapper(x):
            return function(radians(x))

        def radian_wrapper(x):
            return degree(function(x))

        if sw:
            return degree_wrapper
        else:
            return radian_wrapper

    def __tri(self, fn, number):
        """Wrapper for numbers"""
        if self.is_degree:
            if fn:
                # cos, sin, tan
                return math.radians(number)
            else:
                # acos, asin, atan
                return math.degrees(number)
        return number

    # Goniometricke funkcie
    def cos(self, number):
        """Sine function"""
        return math.cos(self.__tri(True, number))

    def sin(self, number):
        """Cosine function"""
        return math.sin(self.__tri(True, number))

    def tan(self, number):
        """Tangent function"""
        return math.tan(self.__tri(True, number))

    def acos(self, number):
        """Arc sine function"""
        return self.__tri(False, math.acos(number))

    def asin(self, number):
        """Arc cosine function"""
        return self.__tri(False, math.asin(number))

    def atan(self, number):
        """Arc tangent function"""
        return self.__tri(False, math.atan(number))

    # sqrt
    @staticmethod
    def sqrt(number):
        """Square root function"""
        return math.sqrt(number)

    @staticmethod
    def root(power, number):
        """Root function"""
        return math.pow(number, 1/power)

    @staticmethod
    def log(number):
        """Natural logarithm function"""
        return math.log(number)

    @staticmethod
    def log10(number):
        """Decadic logarithm function"""
        return math.log10(number)

    @staticmethod
    def factorial(number):
        """Factorial function"""
        return math.factorial(number)

    @staticmethod
    def abs(number):
        """Absolute value function"""
        return abs(number)

    @staticmethod
    def sum(array):
        """Sum function"""
        return sum(array)

    @staticmethod
    def linear_solve(eq1, eq2, eq3, res):
        """Function for solving system of linear equalations"""
        ars = np.array([eq1, eq2, eq3])
        rs = np.array(res)
        try:
            return np.linalg.solve(ars, rs).tolist()
        except:
            return None

    def __make_dicts(self):
        self.trigon = {'cos': self.cos,
                       'sin': self.sin,
                       'tan': self.tan}
        self.atrigon = {'acos': self.acos,
                        'asin': self.asin,
                        'atan': self.atan}
        self.functions = {'sqrt': self.sqrt,
                          'log': self.log,
                          'log10': self.log10,
                          'fact': self.factorial,
                          'abs': self.abs,
                          'root': self.root}
