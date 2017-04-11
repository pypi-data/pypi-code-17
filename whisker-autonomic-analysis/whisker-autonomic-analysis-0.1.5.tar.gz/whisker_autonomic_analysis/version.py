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

VERSION = "0.1.5"  # use semantic version system
VERSION_DATE = "2017-04-11"

VERSION_HISTORY = """

- 0.1.4 (2017-03-14): released.

- 0.1.5 (2017-04-11): added facility to process only sessions found in a
  manually curated master table.
  Table name is SessionsForAutonomicAnalysis (q.v.), which needs the same
    - DateTimeCode
    - Subject
    - Box
  columns as the Config table.

"""