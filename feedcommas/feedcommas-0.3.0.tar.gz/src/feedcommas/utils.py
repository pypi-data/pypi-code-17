# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Utility functions'''

import os
import sys
import errno
from datetime import datetime as dt
from subprocess import Popen, PIPE


def eprint(*args, **kwargs):
    '''Print to stderr.'''
    print(*args, file=sys.stderr, **kwargs)


# pylint: disable=invalid-name
def UNUSED(param):
    '''Mark unused parameters and variables'''
    del param


def get_password_cmd(cmd):
    '''Returns a tuple of command success, command's stdout and stderr.'''
    enc = sys.stdout.encoding
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    out = out.decode(enc).rstrip('\r\n')
    err = err.decode(enc).rstrip('\r\n')

    return (proc.returncode == 0, out, err)


def mkdir_p(path):
    '''Works like `mkdir -p`: creates all (not yet existing) directories in a
    given path.'''
    if not path:
        return

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def now_ts():
    '''Returns timestamp(datetime.now())'''
    return dt.timestamp(dt.now())
