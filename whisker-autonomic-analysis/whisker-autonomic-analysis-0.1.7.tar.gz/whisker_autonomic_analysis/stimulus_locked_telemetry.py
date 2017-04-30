#!/usr/bin/env python
# whisker_autonomic_analysis/stimulus_locked_telemetry.py

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

from typing import Generator, List

from .config import Config
from .heartbeat import Heartbeat
from .lang import auto_repr
from .maths import to_db_float
from .telemetry_means import TelemetryMeans
from .trial_telemetry_record import TrialTelemetryRecord
from .trial_timing import TrialTiming


class StimulusLockedTelemetry(object):
    def __init__(self,
                 telemetry: List[Heartbeat],
                 trial_timing: TrialTiming,
                 cfg: Config,
                 peak_filename: str) -> None:
        # This function is a bit inelegant; it presupposes a certain way of
        # dividing up time. This is the bit of this program that is most tied
        # to a specific behavioural task.
        #
        # The code follows Laith's; the only generalization is chunk_s being
        # a variable (and that we don't do the same thing multiple times to
        # measure multiple variables).
        #
        # Note that the subtraction measures are redundant (they could be
        # calculated by the user from the other data) but are provided as
        # a convenience, and marked as being "difference" data in the database.
        #
        # WE ASSUME that the baseline runs from the baseline start time to the
        # CS onset time.
        #
        # The baseline and CS are sliced into two;
        #   (1) start -> (end - chunk_duration)
        #   (2) (end - chunk_duration) -> end

        self.trial_timing = trial_timing
        self.peak_filename = peak_filename
        self.phases = {}  # Dict[str, TelemetryMeans]

        def add_directly(phase: str, tm: TelemetryMeans) -> None:
            self.phases[phase] = tm

        def add_phase(phase: str,
                      start_time_s: float,
                      end_time_s: float) -> TelemetryMeans:
            tm = TelemetryMeans(cfg=cfg,
                                telemetry=telemetry,
                                start_time_s=start_time_s,
                                end_time_s=end_time_s)
            add_directly(phase, tm)
            return tm

        chunk_dur_s = trial_timing.get_chunk_duration_s()

        # Some of these we'll use for comparison, so make temporary copies.

        baseline_end_time_s = trial_timing.cs_on_time_s

        baseline = add_phase(
            'baseline',
            start_time_s=trial_timing.baseline_start_time_s,
            end_time_s=baseline_end_time_s)
        cs = add_phase(
            'CS',
            start_time_s=trial_timing.cs_on_time_s,
            end_time_s=trial_timing.cs_off_time_s)
        us = add_phase(
            'US',
            start_time_s=trial_timing.us_on_time_s,
            end_time_s=trial_timing.us_off_time_s)

        baseline_split_time_s = max(trial_timing.baseline_start_time_s,
                                    baseline_end_time_s - chunk_dur_s)
        add_phase(
            'baseline_1',
            start_time_s=trial_timing.baseline_start_time_s,
            end_time_s=baseline_split_time_s)
        baseline_2 = add_phase(
            'baseline_2',
            start_time_s=baseline_split_time_s,
            end_time_s=baseline_end_time_s)

        cs_split_time_s = max(trial_timing.cs_on_time_s,
                              trial_timing.cs_off_time_s - chunk_dur_s)
        cs_1 = add_phase(
            'CS_1',
            start_time_s=trial_timing.cs_on_time_s,
            end_time_s=cs_split_time_s)
        cs_2 = add_phase(
            'CS_2',
            start_time_s=cs_split_time_s,
            end_time_s=trial_timing.cs_off_time_s)

        n_chunks = trial_timing.get_n_us_chunks()
        us_chunks = []  # type: List[TelemetryMeans]
        for chunk_index in range(n_chunks):
            chunk_num = chunk_index + 1
            us_chunks.append(add_phase(
                "US_{}".format(chunk_num),
                start_time_s=min(
                    trial_timing.us_on_time_s + chunk_index * chunk_dur_s,
                    trial_timing.us_off_time_s
                ),
                end_time_s=min(
                    (trial_timing.us_on_time_s +
                     (chunk_index + 1) * chunk_dur_s),
                    trial_timing.us_off_time_s
                )
            ))

        add_directly('CS_directed', cs - baseline)
        add_directly('US_directed', us - cs)

        add_directly('CS_directed_1', cs_1 - baseline_2)
        add_directly('CS_directed_2', cs_2 - baseline_2)

        for chunk_index in range(n_chunks):
            chunk_num = chunk_index + 1
            add_directly(
                "US_directed_{}".format(chunk_num),
                us_chunks[chunk_index] - cs_2
            )

    def __repr__(self) -> str:
        return auto_repr(self)

    def gen_trial_telemetry_records(self) -> Generator[TrialTelemetryRecord,
                                                       None, None]:
        tt = self.trial_timing
        sd = tt.session_definition
        for phase_tm in self.phases.items():
            # Process tuple, then split, so the type checker knows...
            phase = phase_tm[0]  # type: str
            tm = phase_tm[1]  # type: TelemetryMeans
            is_difference = tm.is_difference
            for ap, value in tm.get_parameters().items():
                yield TrialTelemetryRecord(
                    date_time=sd.date_time,
                    subject=sd.subject,
                    box=sd.box,

                    trial=tt.trial_number,
                    peak_filename=self.peak_filename,
                    phase=phase,

                    start_time_s=tm.start_time_s,
                    end_time_s=tm.end_time_s,
                    autonomic_parameter=ap,
                    parameter_value=to_db_float(value),
                    is_difference=is_difference,
                )
