"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from logger import log
import subprocess

def netns_add(name):
    call(['sudo', 'ip', 'netns', 'add', name])


def netns_delete(name):
    # TODO: check if ns contains any pids
    call(['sudo', 'ip', 'netns', 'delete', name])


def call(command, shell=False, stdin=None, stdout=None, stderr=None, env=None, retcode=None, netns=None, background=False):
    '''
    Call command
    '''
    if shell is False and netns is not None:
        #TODO: Potential weakness. Command in namespaces are executed as root (via sudo)
        cmd = ['sudo',
               'ip',
               'netns',
               'exec',
               netns]
        cmd.extend(command)
        command = cmd
    elif shell is True and netns is not None:
        # Potential command injection by pipe or stream redirection
        log(msg="Calling command %s with shell=True and non-default network namespace!" % command, tags=('system', 'error'))
        raise Exception('call_error')

    if shell is True:
        log(msg="executing: %s" % command, tags=('system', 'info'))
    else:
        log("executing: %s" % ' '.join(command), tags=('system', 'info'))

    if not background:
        r = subprocess.call(command, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr, env=env)

        if (retcode is not None and r != retcode) or (retcode is None and r != 0):
            log(msg="  Return code: %d" % r, tags=('system', 'info'))

        if retcode is not None and r != retcode:
            raise Exception('call_error')

        return r
    else:
        p = subprocess.Popen(command, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr, env=env)
        return p.pid