#!/usr/bin/env python
# whisker_autonomic_analysis/stimulus_bp.py

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

- Program to analyse, jointly,
  (1) "Peak" files, created like this:
        - telemetry device measuring blood pressure
        -> Spike software
        -> filter (written by Katrin Braesicke, in Spike) to remove
           non-physiological outliers
        -> text file

  (2) Stimulus timing information, either as textfile or relational database
      output from a specific Whisker task, AversivePavlovian (originally
      written by KB, then recoded by Rudolf Cardinal).

- First version: 2017-03-10.

- Note that we have no absolutely reliable way to predict "peak" file names.
  So we offer the user a manual choice, via a GUI.

- REFERENCES

[1]  https://en.wikipedia.org/wiki/Heart_rate_variability
[2]  Allen 2002
     http://apsychoserver.psych.arizona.edu/JJBAReprints/SPR2002/Allen_SPR2002.pdf
[3]  Allen
     http://apsychoserver.psych.arizona.edu/JJBAReprints/CMet/How%20to%20Reduce%20ekg%20data.htm
[4]  Toichi et al. 1997
     https://www.ncbi.nlm.nih.gov/pubmed/9021653
[5]  Lorenz 1963 "Deterministic nonperiodic flow"
     http://dx.doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2
[6]  https://en.wikipedia.org/wiki/Poincar%C3%A9_plot
[7]  Grossman P
     https://www.researchgate.net/post/Is_there_a_standardized_method_for_measuring_vagal_tone
[8]  https://en.wikipedia.org/wiki/Unevenly_spaced_time_series
[9]  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1564191/
[10] HRV Toolkit
     https://physionet.org/tutorials/hrv-toolkit/

- TO DO:

*** Check scaling of output variables.
    For example: ln_rsa: was it expecting its IBIs in s, or ms? Etc.

*** Finish adding support for HRV Toolkit (requires extra tools that it looks for)

"""  # noqa

# Python standard library
import argparse
import logging
import os

# Third-party imports
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# Imports from this package
from .aversive_pavlovian_database import (gen_session_definitions,
                                          process_session)
from .config import Config
from .debugging import pdb_run
from .logsupport import main_only_quicksetup_rootlogger
from .sqlalchemy_base import Base
from .test_filters import test_filters
from .spike_file import test_spike_read
from .version import VERSION, VERSION_DATE

log = logging.getLogger(__name__)


# =============================================================================
# Constants
# =============================================================================

LOG_EQUISPACED_TEST_FREQS = [
    (0.01, 1),
    # (0.0316, 1),
    (0.1, 1),
    # (0.316, 1),
    # (1, 1),
    # (3.16, 1),
]
LINEAR_EQUISPACED_TEST_FREQS = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
]


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    main_only_quicksetup_rootlogger()
    thisdir = os.path.abspath(os.path.dirname(__file__))

    # Command-line arguments
    progtitle = (
        "whisker_autonomic_analysis, "
        "version {version} ({version_date}), by Rudolf Cardinal.".format(
            version=VERSION, version_date=VERSION_DATE))
    progdesc = progtitle + (
        " Takes data from (1) the database created by the AversivePavlovian "
        "Whisker behavioural task, and (2) Spike output of blood pressure "
        "telemetry data. Then (3) creates stimulus-related measures of "
        "autonomic activity, and (4) stashes them back in the database."
    )
    parser = argparse.ArgumentParser(
        description=progdesc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # General settings

    parser.add_argument(
        '--version', action='store_true',
        help="Print version (and stop).",
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help="Be verbose.",
    )

    # Database settings

    dbgroup = parser.add_argument_group('Database', 'Database settings')
    dbgroup.add_argument(
        '--dburl',
        help="Specify the SQLAlchemy URL to find the AversivePavlovian "
             "database",
    )
    dbgroup.add_argument(
        '--skip_if_results_exist', action='store_true',
        help="Skip any sessions (in the database) for which any telemetry "
             "results already exist"
    )
    dbgroup.add_argument(
        '--no_skip_if_results_exist', action='store_false',
        dest='skip_if_results_exist',
        help="Opposite of --skip_if_results_exist: if telemetry results "
             "exist, delete existing results and redo",
    )
    dbgroup.set_defaults(skip_if_results_exist=True)

    # Spike data settings

    spikegroup = parser.add_argument_group(
        'Spike', 'Settings for loading Spike autonomic data files')
    spikegroup.add_argument(
        '--peakdir', default=thisdir,
        help="Specify the directory where Spike peak files live "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--sanity_checks', action='store_true',
        help="Check for e.g. big gaps in telemetry during Spike file loading",
    )
    spikegroup.add_argument(
        '--no_sanity_checks', dest='sanity_checks', action='store_false',
        help="Opposite of --sanity_checks",
    )
    spikegroup.set_defaults(sanity_checks=True)
    spikegroup.add_argument(
        '--sanity_max_rr_discrepancy_s', type=float, default=10,
        help="For sanity checks: maximum permitted R-R discrepancy between "
             "times of consecutive beats and stated IBI (s) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--validate', action='store_true',
        help="Validate during Spike file loading",
    )
    spikegroup.add_argument(
        '--no_validate', dest='validate', action='store_false',
        help="Opposite of --validate",
    )
    spikegroup.set_defaults(validate=True)
    spikegroup.add_argument(
        '--validate_verbose', action='store_true',
        help="Report all data read during Spike file loading",
    )
    spikegroup.add_argument(
        '--valid_bp_min_mmhg', type=float, default=10,
        help="For validation: minimum blood pressure (mmHg) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_bp_max_mmhg', type=float, default=300,
        help="For validation: maximum blood pressure (mmHg) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_hr_min_bpm', type=float, default=10,
        help="For validation: minimum heart rate (beats per minute) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_hr_max_bpm', type=float, default=600,  # it does go over 410!
        help="For validation: maximum heart rate (beats per minute) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_max_hr_error_bpm', type=float, default=1,
        help="For validation: maximum permissible discrepancy between heart "
             "rate stated and heart rate calculated from interbeat interval "
             "(bpm)",
    )

    # HRV calculations

    hrvgroup = parser.add_argument_group(
        'HRV', 'Settings for built-in heart-rate variability calculations')
    hrvgroup.add_argument(
        '--hrv', action='store_true',
        help="Add heart-rate variability (HRV) measures, either using built-in"
             " calculations or external tools",
    )
    hrvgroup.add_argument(
        '--no_hrv', dest='hrv', action='store_false',
        help="Opposite of --hrv",
    )
    hrvgroup.set_defaults(hrv=True)
    hrvgroup.add_argument(
        '--hrv_builtin', action='store_true',
        help="Add built-in HRV measures",
    )
    hrvgroup.add_argument(
        '--no_hrv_builtin', dest='hrv_builtin', action='store_false',
        help="Opposite of --hrv_builtin",
    )
    hrvgroup.set_defaults(hrv_builtin=True)
    hrvgroup.add_argument(
        '--hrv_resample_freq_hz', type=float, default=10,
        help="Resampling frequency to create time series from interbeat "
             "intervals (IBIs), for some heart rate variability (HRV) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_low_cutoff_hz', type=float, default=0.12,
        help="Low frequency cutoff for bandpass filter (amplitude is 0.5 "
             "at this frequency) for respiratory sinus arrhythmia (RSA) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_high_cutoff_hz', type=float, default=0.4,
        help="High frequency cutoff for bandpass filter (amplitude is 0.5 "
             "at this frequency) for respiratory sinus arrhythmia (RSA) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_numtaps', type=int, default=241,
        help="Number of taps for the fixed-impulse-response (FIR) filter used "
             "for RSA analysis",
    )

    # External tool settings

    toolgroup = parser.add_argument_group('Tools', 'External tool settings')
    toolgroup.add_argument(
        '--get_hrv_filename',
        help="Specify the path to the get_hrv tool (from the HRV Toolkit, "
             "https://physionet.org/tutorials/hrv-toolkit/)",
    )
    toolgroup.add_argument(
        '--cd_to_get_hrv', action='store_true',
        help="Change to the directory of the get_hrv tool to run it?",
    )
    toolgroup.add_argument(
        '--no_cd_to_get_hrv', dest='cd_to_get_hrv', action='store_false',
        help="Opposite of --cd_to_get_hrv",
    )
    toolgroup.set_defaults(cd_to_get_hrv=True)  # doesn't help under Linux; use the PATH instead  # noqa

    # Testing

    testgroup = parser.add_argument_group('Test', 'Options for testing')
    testgroup.add_argument(
        '--test_filters', action='store_true',
        help="Test filter system (then stop)",
    )
    testgroup.add_argument(
        '--test_spike',
        help="Specify a Spike output filename to test with (then stop)",
    )
    testgroup.add_argument(
        '--test_start_time_s', type=float,
        help="Start time (s) [INCLUSIVE] to analyse test Spike data (if you "
             "don't specify test_start_time_s / test_end_time_s, the whole "
             "file will be used)",
    )
    testgroup.add_argument(
        '--test_end_time_s', type=float,
        help="End time (s) [EXCLUSIVE] to analyse test Spike data (if you "
             "don't specify test_start_time_s / test_end_time_s, the whole "
             "file will be used)",
    )

    progargs = parser.parse_args()
    if progargs.version:
        print("VERSION: {}\nVERSION_DATE: {}".format(VERSION, VERSION_DATE))
        return
    log.setLevel(logging.DEBUG if progargs.verbose else logging.INFO)
    log.info(progtitle)
    log.debug("Arguments: {}".format(progargs))

    def abspath_if_given(x):
        return os.path.abspath(x) if x else ''

    db_required = not (progargs.test_filters or progargs.test_spike)

    # Create config object
    if db_required:
        # Database connection required
        if not progargs.dburl:
            raise ValueError("Database URL not specified. Try --help.")
        engine = create_engine(progargs.dburl)
        log.info("Connected to database: {}".format(engine))  # hides password
        log.info("Creating any output tables that don't exist...")
        Base.metadata.create_all(engine)
        connection = engine.connect()
        session = sessionmaker(bind=engine)()
    else:
        # No database connection required
        engine = None
        connection = None
        session = None
    cfg = Config(
        connection=connection,
        engine=engine,
        hrvtk_cd_to_get_hrv=progargs.cd_to_get_hrv,
        hrvtk_get_hrv_filename=abspath_if_given(progargs.get_hrv_filename),
        hrv=progargs.hrv,
        hrv_builtin=progargs.hrv_builtin,
        hrv_resample_freq_hz=progargs.hrv_resample_freq_hz,
        peak_dir=progargs.peakdir,
        rsa_high_cutoff_hz=progargs.rsa_high_cutoff_hz,
        rsa_low_cutoff_hz=progargs.rsa_low_cutoff_hz,
        rsa_numtaps=progargs.rsa_numtaps,
        sanity_checks=progargs.sanity_checks,
        sanity_max_rr_discrepancy_s=progargs.sanity_max_rr_discrepancy_s,
        session=session,
        skip_if_results_exist=progargs.skip_if_results_exist,
        test_end_time_s=progargs.test_end_time_s,
        test_spike_filename=abspath_if_given(progargs.test_spike),
        test_start_time_s=progargs.test_start_time_s,
        validate=progargs.validate,
        valid_bp_min_mmhg=progargs.valid_bp_min_mmhg,
        valid_bp_max_mmhg=progargs.valid_bp_max_mmhg,
        valid_hr_min_bpm=progargs.valid_hr_min_bpm,
        valid_hr_max_bpm=progargs.valid_hr_max_bpm,
        valid_max_hr_error_bpm=progargs.valid_max_hr_error_bpm,
        validate_verbose=progargs.validate_verbose,
    )
    log.info("Configuration:\n{}".format(cfg))

    # Do a test run and quit?
    if progargs.test_filters:
        test_filters(cfg, freq_amp_pairs=LOG_EQUISPACED_TEST_FREQS,
                     show_filter_response=True)
        test_filters(cfg, freq_amp_pairs=LINEAR_EQUISPACED_TEST_FREQS)
        return
    if progargs.test_spike:
        test_spike_read(cfg)
        return

    # Process all sessions found in database
    # noinspection PyTypeChecker
    log.info("Processing available sessions.")
    if cfg.skip_if_results_exist:
        log.info("... skipping any sessions for which telemetry data exists")
    count = 0
    # noinspection PyTypeChecker
    for session_definition in gen_session_definitions(cfg):
        process_session(cfg=cfg, session_definition=session_definition)
        count += 1
    log.info("All sessions processed: count = {}.".format(count))


# =============================================================================
# Command-line entry point
# =============================================================================

if __name__ == '__main__':
    with_pdb = False  # for debugging only
    if with_pdb:
        pdb_run(main)
    else:
        main()
