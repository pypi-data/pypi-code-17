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

import random


def integer(function, floor, ceiling):
    """ Returns a random integer between (and including) and the provided floor and ceiling parameters.

    The returned integer lies within the range [floor, ceiling].  The provided function determines how the values
    in the range will be weighted.  Important note, this is pseudo-random.

    :param function: defines the weight assigned to the range of integers
    :type function: Function as defined in __init__.py
    :param floor: minimum random value
    :type floor: int
    :param ceiling: maximum random value
    :rtype ceiling: int
    :return: weighted random value
    :rtype: int
    :raises: ValueError if floor > ceiling
    """
    assert type(floor) is int
    assert type(ceiling) is int

    if floor > ceiling:
        raise ValueError('floor %d must be greater than ceiling %d' % (floor, ceiling))

    if floor == ceiling:
        return floor

    # fairly simple algorithm, sums all the weights, chooses a random value between 0 and summation, and iterates
    # to find the index of the value that surpasses the random value.  That will match the choice.

    weights = [function.evaluate(i) for i in xrange(floor, ceiling+1)]
    total = sum(weights)

    selection = random.uniform(0, total)
    agg = 0
    for i, value in enumerate(xrange(floor, ceiling+1)):
        agg += weights[i]
        if agg >= selection:
            return value

    raise RuntimeError('error in weighted code')
