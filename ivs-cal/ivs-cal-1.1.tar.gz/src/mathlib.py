#!/usr/bin/env python3

from math import *
import string


class solver():

    def __init__(self):
        # Variables
        self.ans = 0
        self.variables = {}
        for letter in string.ascii_uppercase:
            self.variables[letter] = 0
        self.variables['ans'] = self.ans

        # Constants
        self.constants = {'pi': pi, 'e': e}

        # Functions
        self.sqrt = sqrt
        self.log = log
        self.log10 = log10
        self.factorial = factorial
        self.abs = abs

        # Trigonometric functions
        self.is_degree = False
        self.cos = cos
        self.sin = sin
        self.tan = tan
        self.acos = acos
        self.asin = asin
        self.atan = atan

        self.__make_dicts()

    def switch_rad_deg(self):
        self.cos = cos if self.is_degree else self.__switch(True, cos)
        self.sin = sin if self.is_degree else self.__switch(True, sin)
        self.tan = tan if self.is_degree else self.__switch(True, tan)
        self.acos = acos if self.is_degree else self.__switch(False, acos)
        self.asin = asin if self.is_degree else self.__switch(False, asin)
        self.atan = atan if self.is_degree else self.__switch(False, atan)
        self.is_degree = not self.is_degree

    def solve(self, text):
        try:
            self.ans = eval(text, {}, {**self.variables,
                                       **self.constants,
                                       **self.functions,
                                       **self.trigon,
                                       **self.atrigon})
            return self.ans
        except ZeroDivisionError as e:
            return ZeroDivisionError

    def std(self, x):
        return sqrt(1/(len(x)-1)*(sum([a**2 for a in x]) - sum(x)**2/len(x)))

    def store(self, cls):
        def storing(name, value):
            cls.variables[name] = value
            return value
        return storing

    def __switch(self, sw, function):
        def degree_wrapper(x):
            return function(radians(x))

        def radian_wrapper(x):
            return degree(function(x))

        if sw:
            return degree_wrapper
        else:
            return radian_wrapper

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
                          'store': self.store(self)}
