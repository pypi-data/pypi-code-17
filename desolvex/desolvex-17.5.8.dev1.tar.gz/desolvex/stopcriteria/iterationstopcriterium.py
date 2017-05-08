# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


class IterationStopCriterion(object):

    def __init__(self, variables_dict, maximum_iterations):

        self.__maximum_iterations = maximum_iterations
        self.__variables_dict = variables_dict
        self.__variables_dict['iteration'] = 0

    @property
    def int_maximum(self):
        return self.__maximum_iterations

    @property
    def int_value(self):
        return self.__variables_dict['iteration']

    def met(self):

        if self.__variables_dict['iteration'] < self.__maximum_iterations:
            return False

        return True

    def update(self):
        self.__variables_dict['iteration'] += 1

