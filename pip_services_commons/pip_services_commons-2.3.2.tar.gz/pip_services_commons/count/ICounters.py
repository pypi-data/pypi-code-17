# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.ICounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for performance counters components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICounters:
    """
    Interface for performance counters. These components
    are used to measure non-functional characteristics
    of microservice components: number of calls,
    execution time, timing of key events, etc.
    """

    def begin_timing(self, name):
        """
        Starts measurement of execution time interval.
        The method returns ITiming object that provides endTiming()
        method that shall be called when execution is completed
        to calculate elapsed time and update the counter.

        Args:
            name: the name of interval counter.

        Returns: ITiming callback interface with endTiming() method that shall be called at the end of execution.
        """
        raise NotImplementedError('Method from interface definition')

    def stats(self, name, value):
        """
        Calculates rolling statistics: minimum, maximum, average
        and updates Statistics counter.
        This counter can be used to measure various non-functional
        characteristics, such as amount stored or transmitted data,
        customer feedback, etc.

        Args: 
            name: the name of statistics counter.
            value: the value to add to statistics calculations.

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def last(self, name, value):
        """
        Records the last reported value. 
        This counter can be used to store performance values reported
        by clients or current numeric characteristics such as number
        of values stored in cache.
        
        Args:
            name: the name of last value counter
            value: the value to be stored as the last one

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def timestamp_now(self, name):
        """
        Records the current time.
        This counter can be used to track timing of key business transactions.

        Args:
            name: the name of timing counter

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def timestamp(self, name, value):
        """
        Records specified time.
        This counter can be used to tack timing of key
        business transactions as reported by clients.
        
        Args:
            name: the name of timing counter.
            value: the reported timing to be recorded.

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def increment_one(self, name):
        """
        Increments counter by value of 1.
        This counter is often used to calculate
        number of client calls or performed transactions.

        Args:
            name: the name of counter counter.

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def increment(self, name, value):
        """
        Increments counter by specified value.
        This counter can be used to track various numeric characteristics

        Args:
            name: the name of the increment value.
            value: number to increase the counter.

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')
