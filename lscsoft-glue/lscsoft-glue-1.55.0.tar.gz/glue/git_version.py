id = "b2a15440207a19f0dbf40ea6042f20dc5b4a24c6"
date = "2017-04-06 21:11:47 +0000"
branch = "master"
tag = "None"
if tag == "None":
    tag = None
author = "Duncan Brown <duncan.brown@ligo.org>"
builder = "Duncan Brown <duncan.brown@ligo.org>"
committer = "Duncan Brown <duncan.brown@ligo.org>"
status = "CLEAN: All modifications committed"
version = id
verbose_msg = """Branch: master
Tag: None
Id: b2a15440207a19f0dbf40ea6042f20dc5b4a24c6

Builder: Duncan Brown <duncan.brown@ligo.org>
Build date: 2017-04-06 21:13:08 +0000
Repository status: CLEAN: All modifications committed"""

import warnings

class VersionMismatchError(ValueError):
    pass

def check_match(foreign_id, onmismatch="raise"):
    """
    If foreign_id != id, perform an action specified by the onmismatch
    kwarg. This can be useful for validating input files.

    onmismatch actions:
      "raise": raise a VersionMismatchError, stating both versions involved
      "warn": emit a warning, stating both versions involved
    """
    if onmismatch not in ("raise", "warn"):
        raise ValueError(onmismatch + " is an unrecognized value of onmismatch")
    if foreign_id == "b2a15440207a19f0dbf40ea6042f20dc5b4a24c6":
        return
    msg = "Program id (b2a15440207a19f0dbf40ea6042f20dc5b4a24c6) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)

