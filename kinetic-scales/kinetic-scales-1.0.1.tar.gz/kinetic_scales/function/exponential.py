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

import math

from ..weighted import Function


class Exponential(Function):
    """ Implements an exponential based algorithm for evaluation.

    Tends to have tighter drop offs than hyperbolic algorithm.
    """
    def __init__(self, scalar=1):
        """Scalar is a user-defined adjustment that can be made to the slope of the exponential algorithm.
        High scalars will result in steeper drops and a shorter tail.  Small scalars (ie, .1) will result in a
        linear-looking graph with a very long tail.  The scalar can also be used to determine direction of the slope,
        ie, using a negative scalar.

        :param scalar: user-defined slope adjustment
        :type scalar: int or long or float
        """
        self._scalar = scalar

    def evaluate(self, value):
        """Returns e**(scalar * value).

        :param value: value to use as the exponent to e
        :type value: int or long or float
        :return: float
        """
        return math.exp(self._scalar * value)
