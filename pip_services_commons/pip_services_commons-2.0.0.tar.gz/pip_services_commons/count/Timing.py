# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.Timing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Timing implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

class Timing:
    """
    Provides callback to end measuring execution time interface and update interval counter.
    """

    _start = None
    _callback = None
    _counter = None

    def __init__(self, counter = None, callback = None):
        """
        Creates instance of timing object that calculates elapsed time
        and stores it to specified performance counters component under specified name.

        Args:
            counter: a name of the counter to record elapsed time interval.
            callback: a performance counters component to store calculated value.
        """

        self._counter = counter
        self._callback = callback
        self._start = time.clock() * 1000

    def end_timing(self):
        """
        Completes measuring time interval and updates counter.
        """

        if self._callback != None:
            elapsed = time.clock() * 1000 - self._start
            self._callback.end_timing(self._counter, elapsed)