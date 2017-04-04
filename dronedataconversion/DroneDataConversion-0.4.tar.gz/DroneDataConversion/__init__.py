# DroneDataConversion
#
# Copyright (C) 2016 Johannes Kinzig
# Author: Johannes Kinzig <johannes_kinzig@icloud.com>
# URL: <https://johanneskinzig.de/software-development/python-parser-bebop-logs.html>
#
# $Id: __init__.py 0003 20016-06-12 jokinzig $

"""
When flying the Parrot Bebop Quadcopter (and the Bebop 2 Quadcaopter) stores all flight information in a log file. This is a so called pud file and has a json structure.

This pud file includes detailed flight information which is also used by Parrot to store the flights in their cloud (formerly known as ARDrone Academy, Drone Academy) and to perform the flight analysis, such as generating battery plot, speed plot and altitude plot.

This library allows to extract important flight information from the pud file. The data in the pud file (flight log) is processed and can then be used for further flight analysis.

Supported Operating Systems:
The library was written and tested under OS X and Unix. No special libraries or expressions were used which prevent running the library under Windows. But note, it is untested.

Python Interpreter:
This library was written using legacy Python 2.7.10. At the current state it is untested under Python 3 and will most likely run under Python 2.7. only


Package Organization
====================


@author: Johannes Kinzig <johannes_kinzig@icloud.com>
@requires: Python 2.7.10+
@version: 0.4
@see: https://johanneskinzig.de/software-development/python-parser-bebop-logs.html>

@todo: export as kml file    DroneDataConversion.py    /DroneDataConversion    line 267    Task
@todo: Improve documentation and epydoc generation

@bug: battery percentage is only correct when flight began with 100% battery charge

@license: Apache License, Version 2.0
@copyright: 2016 Johannes Kinzig

@newfield contributor: Contributor, Contributors (Alphabetical Order)
@contributor: Johannes Kinzig  <mailto:johannes_kinzig@icloud.com>

"""
__docformat__ = 'epytext en'

__version__ = '0.4'
"""The version of DroneDataConversion"""

__author__ = 'Johannes Kinzig <johannes_kinzig@icloud.com>'
"""The primary author of DroneDataConversion"""

__url__ = 'https://johanneskinzig.de/software-development/python-parser-bebop-logs.html'
"""The URL for DroneDataConversion's homepage"""

__license__ = 'Apache License, Version 2.0'
"""The license governing the use and distribution of DroneDataConversion"""

# [xx] this should probably be a private variable:
DEBUG = False
"""True if debugging is turned on."""