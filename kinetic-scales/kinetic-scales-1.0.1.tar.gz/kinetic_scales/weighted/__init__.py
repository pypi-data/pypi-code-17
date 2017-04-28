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

import abc

from .integer import integer


__all__ = [
    integer
]


class Function(object):
    """Used to define functions that can be evaluated to weight selections.

    Function defines the abstract class that must be provided to the various
    weighted capabilities available in this package.  It defines a single method
    that all provided functions must implement.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, value):
        pass
