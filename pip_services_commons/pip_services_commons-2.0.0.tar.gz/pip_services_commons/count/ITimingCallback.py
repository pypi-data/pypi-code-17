# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.ITimingCallback
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for performance timing callbacks.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ITimingCallback:
    """
    Interface for Timing callbacks to record captured elapsed time
    """

    def end_timing(self, name, elapsed):
        """
        Recording calculated elapsed time

        Args:
            name: he name of the counter
            elapsed: time in milliseconds
        """
        raise NotImplementedError('Method from interface definition')
