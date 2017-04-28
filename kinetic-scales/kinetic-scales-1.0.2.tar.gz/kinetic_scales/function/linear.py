# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from ..weighted import Function


class Linear(Function):
    """ Implements an linear-based algorithm for evaluation.

    Tends to have the lightest drop-off of all.
    """
    def __init__(self, slope=1, y_intercept=0):
        """Initialize defining the slope of the line and the y-intercept.  In this form, the weight = mx + b.  Using
        a slope of 0 effectively makes this a constant function that returns the y-intercept.

        :param slope: defines how drastic the curve weights items.
        :type slope: int or long or float
        :param y_intercept: defines some constant offset to apply to the resulting value
        :type y_intercept: int or long or float
        """
        self._slope = slope
        self._y_intercept = y_intercept

    def evaluate(self, value):
        """Evaluates the resulting value on a simple y = mx + b line.

        :param value: the value for x
        :type value: int or long
        :return: y
        :rtype: float
        """
        return float(self._slope) * value + self._y_intercept
