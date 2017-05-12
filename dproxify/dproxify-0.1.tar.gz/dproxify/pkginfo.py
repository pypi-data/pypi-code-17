# dproxify package info
# Written by nature through Francesco Palumbo aka phranz
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


DESCRIPTION = 'An object daemon proxifier for GNU/Linux (Python 3.x)'

LONG_DESC   = '''------------------------------------------------------
dproxify is a object daemon proxifier for GNU/Linux
(Python 3.x), released under the terms of GPL3 license.
-------------------------------------------------------

Any custom object which is pickleable, is loaded
into a detached daemon which communicate with
clients (one at a time) through AFUnix sockets.
With some exceptions (this is an alpha project),
every call to object's methods through client is
executed/computed on the daemon.'''

MODNAME = 'dproxify'
VERSION = '0.1'
LICENSE = 'GNU General Public License v3'
AUTHOR  = 'nature thorugh Francesco Palumbo aka phranz'
EMAIL   = 'franzodev@gmail.com'
REPO    = 'https://github.com/phr4nz/dproxify'
