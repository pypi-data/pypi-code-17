# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:44:29 2015

@author: joseph
"""
import math
import time
import random
import os
import warnings



class is_prime(object):

    def __init__(self, number_that_may_be_prime):
        self.number_that_may_be_prime = number_that_may_be_prime
        self.calculated = False
        self.isPrime = None

    def calculate_safely(self):
        for i in range(2, int(math.sqrt(self.number_that_may_be_prime))):
            if self.number_that_may_be_prime % i == 0:
                self.isPrime = False
                self.calculated = True
                return self
        self.isPrime = True
        self.calculated = True
        return self

    def calculate(self):
        "calculates temperamentally with system errors being thrown"
        if self.calculated:
            return self
        time.sleep(5 * random.random())
        # if random.random() < .2:
        #     raise Exception("Darn you!  I quit")
        # if random.random() < .15:
        #     myPid = os.getpid()
        #     os.system("kill -9 %s" % str(myPid))
        if random.random() < .5:
            warnings.warn("Darn you, I'm on break!")
            time.sleep(10)

        return self.calculate_safely()
