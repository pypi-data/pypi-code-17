#!/usr/bin/env python
# whisker_autonomic_analysis/trial_timing.py

"""
===============================================================================
    Copyright (C) 2017-2017 Rudolf Cardinal (rudolf@pobox.com).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
===============================================================================
"""

import logging
import math
import pprint

from .lang import simple_repr
from .session_definition import SessionDefinition

log = logging.getLogger(__name__)


# =============================================================================
# Processing behavioural task data re CS/US timings
# =============================================================================

class TrialTiming(object):
    def __init__(self,
                 session_definition: SessionDefinition,
                 trial_number: int,
                 baseline_start_time_s: float,
                 cs_on_time_s: float,
                 cs_off_time_s: float,
                 us_on_time_s: float,
                 us_off_time_s: float) -> None:
        self.session_definition = session_definition
        self.trial_number = trial_number
        self.baseline_start_time_s = baseline_start_time_s
        self.cs_on_time_s = cs_on_time_s
        self.cs_off_time_s = cs_off_time_s
        self.us_on_time_s = us_on_time_s
        self.us_off_time_s = us_off_time_s
        # Some checks:
        try:
            assert session_definition is not None
            assert trial_number >= 0
            assert baseline_start_time_s >= 0
            assert cs_on_time_s >= baseline_start_time_s
            assert cs_off_time_s >= cs_on_time_s
            # assert us_on_time_s >= cs_off_time_s  # NO, this can be false happily (CS can co-terminate with US).  # noqa
            assert us_off_time_s >= us_on_time_s
        except AssertionError:
            log.critical(pprint.pformat({
                'session_definition': session_definition,
                'trial_number': trial_number,
                'baseline_start_time_s': baseline_start_time_s,
                'cs_on_time_s': cs_on_time_s,
                'cs_off_time_s': cs_off_time_s,
                'us_on_time_s': us_on_time_s,
                'us_off_time_s': us_off_time_s,
            }))
            raise

    def __repr__(self) -> str:
        return simple_repr(self, ["trial_number", "baseline_start_time_s",
                                  "cs_on_time_s", "cs_off_time_s",
                                  "us_on_time_s", "us_off_time_s"])

    def get_chunk_duration_s(self) -> float:
        return self.session_definition.chunk_duration_s

    def get_n_us_chunks(self) -> int:
        us_time = max(0.0, self.us_off_time_s - self.us_on_time_s)
        chunk_time = self.get_chunk_duration_s()
        n_chunks = math.ceil(us_time / chunk_time)  # type: int
        return n_chunks
