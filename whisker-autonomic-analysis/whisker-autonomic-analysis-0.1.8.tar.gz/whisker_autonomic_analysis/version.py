#!/usr/bin/env python
# whisker_autonomic_analysis/version.py

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

VERSION = "0.1.8"  # use semantic version system
VERSION_DATE = "2017-05-01"

VERSION_HISTORY = """

- 0.1.4 (2017-03-14): released.

- 0.1.5 (2017-04-11): added facility to process only sessions found in a
  manually curated master table.
  Table name is SessionsForAutonomicAnalysis (q.v.), which needs the same
    - DateTimeCode
    - Subject
    - Box
  columns as the Config table.

- 0.1.6 (2017-04-11): removed one incorrect assertion from
  TrialTiming.__init__()
  
- 0.1.7 (2017-04-29): define CS/US timing from database, rather than hard-coded
  - Added ChunkDurationSec (float) to SessionsForAutonomicAnalysis table.
  - So, creation SQL is:
  
    CREATE TABLE SessionsForAutonomicAnalysis (
        DateTimeCode DATETIME NOT NULL,
        Subject VARCHAR(45) NOT NULL,
        Box INT NOT NULL,
        ChunkDurationSec FLOAT NOT NULL
    );
    
    and a quick population command is:
    
    INSERT INTO SessionsForAutonomicAnalysis (
        DateTimeCode,
        Subject,
        Box,
        ChunkDurationSec
    )
    SELECT
        DateTimeCode,
        Subject,
        Box,
        10.0
    FROM Config;

  - Bugfixes for zero-length slices.

- 0.1.8 (2017-05-01): changed the definition of how baseline/CS are split
  into chunks. See StimulusLockedTelemetry.init().

"""
