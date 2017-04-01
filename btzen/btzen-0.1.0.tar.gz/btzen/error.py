#
# BTZen - Bluetooh Smart sensor reading library.
#
# Copyright (C) 2015-2017 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class Error(Exception):
    """
    Base, abstract BTZen exception.
    """

class ConnectionError(Error):
    """
    Connection error.
    """

class ConfigurationError(Error):
    """
    Sensor configuration error.
    """

class DataReadError(Error):
    """
    Sensor data reading error.
    """

# vim: sw=4:et:ai
