# utility functions
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


import sys
import os
import stat
import signal



def error(msg):
    '''
    Exit with an error message.
    '''

    print('[Error]:', msg, file=sys.stderr)
    sys.exit(1)


def create_dirs(dirs):
    '''
    Creates directories if they don't exist.

    Arguments:
    dirs -- A list of directories
    '''

    [os.makedirs(d) for d in dirs if not os.path.isdir(d)]


def cat(fpath):
    '''
    Returns the content of the file at fpath.
    '''

    with open(fpath, 'r') as f:
        return ''.join(f.readlines())


def write(fpath, arg):
    '''
    Write the string representation of
    arg to the file at fpath.
    '''

    arg = str(arg)

    with open(fpath, 'w') as f:
        f.write(arg)


def issocket(fpath):
    '''
    Returns True if file at fpath is a socket, else False.
    '''

    return stat.S_ISSOCK(os.stat(fpath).st_mode)


def isfloat(val):
    '''
    Returns True if val is float, else False.
    '''

    try:
        float(val)
        return True

    except ValueError:
        return False


def daemonize(pidfile, newfds=(None, None, None),
              procedure=lambda: 0, args=(),
              shutdown=lambda: 0, shutargs=(),
              ignored_sigs=()):

    '''
    Daemonizes a procedure. The forked daemon
    is detached and its PID is write to the path
    provided with pidfile.

    Arguments:

    pidfile -- the file path in which to store daemon PID.

    Keywords arguments:

    newfds -- A tuple of three file descriptors which represent
              the new stdin, stdout and stderr (in order).
              All three defaults to 'None', meaning stdin, stdout
              and stderr all points to /dev/null

    procedure -- The procedure to execute.

    args -- Arguments of the procedure.

    shutdown -- The procedure to execute at shutdown.

    shutargs -- Arguments of the shutdown procedure.

    ignored_sigs -- signals to ignore. NOTE: SIGINT and SITERM
                    are alredy handled for the purpose of exiting "gracefully".
    '''


    # fork and parent exit
    if os.fork() > 0:
        return

    # detach and fork
    os.setsid()
    pid = os.fork()

    if pid > 0:
        write(pidfile, pid)
        sys.exit()

    # set file descriptors
    fdnull = None

    if None in newfds:
        fdnull = os.open(os.devnull, os.O_RDWR)

    nfds = [fd if fd is not None else fdnull for fd in newfds]
    sfds = [o.fileno() for o in (sys.stdin, sys.stdout, sys.stderr)]

    for n, s in zip(nfds, sfds):
        os.dup2(n, s)

    # set dir etc.
    os.chdir('/')

    # shutdown/cleanup procedure
    def exit_daemon(sig, stframe):
        shutdown(*shutargs)

        if os.path.exists(pidfile):
            os.remove(pidfile)

        os._exit(0)

    # signal setup
    for s in tuple(*ignored_sigs):
        signal.signal(s, signal.SIG_IGN)

    for s in (signal.SIGINT, signal.SIGTERM):
        signal.signal(s, exit_daemon)

    # daemonized procedure
    procedure(*args)
    exit_daemon(None, None)


def isrunning(pidnum):
    '''
    Returns True if a process that
    maps to pidnum (as string) is running, else None.
    '''

    for p in os.listdir('/proc'):
        if p == pidnum:
            return True
