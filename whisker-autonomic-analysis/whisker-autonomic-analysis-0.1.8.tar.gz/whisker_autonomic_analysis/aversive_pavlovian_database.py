#!/usr/bin/env python
# whisker_autonomic_analysis/aversive_pavlovian_database.py

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
from typing import Generator, List

from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from .config import Config
from .session_definition import SessionDefinition
from .spike_file import fetch_all_telemetry
from .stimulus_locked_telemetry import StimulusLockedTelemetry
from .trial_telemetry_record import TrialTelemetryRecord
from .trial_timing import TrialTiming

log = logging.getLogger(__name__)


def fetch_trial_timings(
        connection: Connection,
        session_definition: SessionDefinition) -> List[TrialTiming]:
    # http://docs.sqlalchemy.org/en/rel_0_9/core/sqlelement.html#sqlalchemy.sql.expression.text  # noqa
    result = connection.execute(
        text("""
SELECT
    Trial,
    TrialStartTimeSec,
    CSStartTimeSec,
    CSStopTimeSec,
    USStartTimeSec,
    USStopTimeSec
FROM
    TrialRecords
WHERE
    DateTimeCode = :date_time_code
    AND Subject = :subject
    AND Box = :box
ORDER BY
    Trial
        """),
        date_time_code=session_definition.date_time,
        subject=session_definition.subject,
        box=session_definition.box,
    )
    trial_timings = []  # type: List[TrialTiming]
    for row in result:
        tt = TrialTiming(session_definition=session_definition,
                         trial_number=row['Trial'],
                         baseline_start_time_s=row['TrialStartTimeSec'],
                         cs_on_time_s=row['CSStartTimeSec'],
                         cs_off_time_s=row['CSStopTimeSec'],
                         us_on_time_s=row['USStartTimeSec'],
                         us_off_time_s=row['USStopTimeSec'])
        trial_timings.append(tt)
    return trial_timings


def delete_existing_results(dbsession: Session,
                            session_definition: SessionDefinition) -> None:
    log.debug("Deleting existing results for session: {}".format(
        session_definition))
    dbsession.query(TrialTelemetryRecord).filter(
        TrialTelemetryRecord.date_time == session_definition.date_time,
        TrialTelemetryRecord.subject == session_definition.subject,
        TrialTelemetryRecord.box == session_definition.box
    ).delete()
    # See also http://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying  # noqa
    log.debug("... commit")
    dbsession.commit()
    log.debug("... done")


def process_session(cfg: Config,
                    session_definition: SessionDefinition) -> None:
    log.info("Processing session: {}".format(session_definition))
    # Fetch data
    trial_timings = fetch_trial_timings(connection=cfg.connection,
                                        session_definition=session_definition)
    spike_peak_filename = session_definition.get_peak_filename()
    telemetry = fetch_all_telemetry(cfg, spike_peak_filename)
    # Do some thinking, and save results to the output database
    if not cfg.skip_if_results_exist:
        delete_existing_results(dbsession=cfg.session,
                                session_definition=session_definition)
    for trial_timing in trial_timings:
        log.info("... processing trial: {}".format(trial_timing))
        slt = StimulusLockedTelemetry(telemetry=telemetry,
                                      trial_timing=trial_timing,
                                      cfg=cfg,
                                      peak_filename=spike_peak_filename)
        # noinspection PyTypeChecker
        for ttr in slt.gen_trial_telemetry_records():
            cfg.session.add(ttr)
    log.debug("... commit")
    cfg.session.commit()
    log.debug("... done")


def gen_session_definitions(cfg: Config) -> Generator[SessionDefinition, None,
                                                      None]:
    sql = """
SELECT
    DateTimeCode,
    Subject,
    Box,
    ChunkDurationSec
FROM
    SessionsForAutonomicAnalysis AS s
    """
    # - Prior to v0.1.5 (2017-04-11), we were selecting from the Config table.
    #   We just replace that with SessionsForAutonomicAnalysis, to have a
    #   manually curated table instead. (It's still aliased to 'c' so we don't
    #   need to change the add-on bit below.)
    # - Added ChunkDurationSec, v0.1.7
    if cfg.skip_if_results_exist:
        sql += """
WHERE NOT EXISTS (
    SELECT * FROM {telemetry_table} AS tt
    WHERE
        tt.date_time = s.DateTimeCode  -- both DATETIME
        AND tt.subject = s.Subject  -- both VARCHAR
        AND tt.box = s.Box  -- both INT
)
        """.format(
            telemetry_table=TrialTelemetryRecord.__tablename__,
        )
    result = cfg.connection.execute(text(sql))
    for row in result:
        yield SessionDefinition(date_time=row[0],
                                subject=row[1],
                                box=row[2],
                                chunk_duration_s=row[3],
                                peakfile_base_dir=cfg.peak_dir)
