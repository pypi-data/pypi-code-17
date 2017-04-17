"""This module contains the TimeTrack"""

import pandas as pd
import numpy as np

from .functions import TimeFunction


ERR_BOUNDARY = "Given time value '{}' is not located within '{}' and '{}' " \
               "boundaries of parent TimeSeries."


class TimeTrackResult:
    """Contains the result of generated TimeTrack instance.
    
    """

    def __init__(self, track, values):
        self.values = values
        self.track = track


class TimeTrack:
    """Defines a concrete time interval from `start` to `end` belonging to 
    a given TimeSeries `time_series`. Each TimeTrack has a TimeFunction 
    `time_function` which provides the actual time series values.
    
    """

    def __init__(self, time_series, time_function=None, percentage=1,
                 default=np.NaN, start=None, end=None, freq=None,
                 iterated=None, condition=None):
        """Initializes TimeTrack objects. 
        
        """

        self.time_series = time_series

        if isinstance(time_function, TimeFunction):
            self.time_function = time_function
        else:
            self.time_function = TimeFunction(vectorized=time_function,
                                              iterated=iterated,
                                              condition=condition)

        self.percentage = percentage
        self.default = default

        if start:
            self.start = self.check_boundaries(time_series, start)
        else:
            self.start = time_series.index.min()

        if end:
            self.end = self.check_boundaries(time_series, end)
        else:
            self.end = time_series.index.max()

        if freq:
            self.freq = freq
        else:
            self.freq = time_series.freq

        self.index = pd.date_range(self.start, self.end, freq=self.freq)


    def generate(self):
        """Populates TimeTracks's time index with concrete time series values 
        provided by the TimeFunction. 

        Return result as a TimeTrackResult.

        """
        generated = []
        generated_cnt, units_used, units_current = 0, 0, 0

        units_total = self.index.shape[0]
        units_free = int(units_total * self.percentage)
        units_spare = units_total - units_free

        # generate values until no free units are available
        while units_used < units_free and units_current < units_total:
            # get current time series index with values
            current_index = self.index[units_current:]
            current_values = np.arange(1, current_index.shape[0] + 1)
            generate_from = pd.Series(current_values, current_index)

            # generate values from time function
            generated_values = self.time_function.generate(generate_from)
            generated.append(generated_values)
            generated_cnt += 1

            # increase unit counter
            units_generated = generated_values.shape[0]
            units_used += units_generated
            units_used_avg = (units_free / (units_used / generated_cnt))
            units_diff = int(units_spare / (units_used_avg + 1))
            units_current += units_generated + units_diff

        # concatenate all sub time series values
        ts_values = pd.concat(generated)

        # add default values if required
        if self.default is not None:
            ts_values = ts_values.asfreq(self.freq).fillna(self.default)

        return TimeTrackResult(self, ts_values)


    def __repr__(self):
        tpl = "{} (start: {}, end: {}, freq: {}, function: {}"
        return tpl.format(self.__class__.__name__,
                          self.start,
                          self.end,
                          self.freq,
                          self.time_function)


    @staticmethod
    def check_boundaries(ts, boundary):
        """Checks if `boundary` time value lies within the start and end values
        of a given TimeSeries `ts`.
        
        """

        boundary = pd.to_datetime(boundary)

        min_boundary = ts.index.min()
        max_boundary = ts.index.max()

        if not min_boundary <= boundary <= max_boundary:
            raise ValueError(ERR_BOUNDARY.format(boundary,
                                                 min_boundary,
                                                 max_boundary))

        return boundary
