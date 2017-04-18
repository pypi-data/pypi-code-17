from _readfile import readfile
from _sshConfig import *
from _writefile import writefile
from _fexecvp import fexecvp
from _fnmatches import fnmatches
from _run_cmd import *
from _defaultify import *
from _isInt import *

import re

__all__ = [
    'defaultify',
    'defaultify',
    'defaultifyDict',
    'defaultifyDict',
    'fexecvp',
    'fnmatches',
    'getSshHost',
    'isInt',
    'isIp',
    'keyscanHost',
    'readSshConfig',
    'readfile',
    'removeKnownHosts',
    'resetKnownHost',
    'resetKnownHosts',
    'run',
    'run_cmd',
    'writefile'
]

def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def isIp(string):
    return None != re.match("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",string)
