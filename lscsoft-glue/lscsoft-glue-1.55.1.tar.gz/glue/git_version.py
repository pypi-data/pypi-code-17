id = "e53000c136f795ef247b0fea9e1ad92d17c563cd"
date = "2017-04-06 22:10:00 +0000"
branch = "master"
tag = "glue-release-1-55-1"
if tag == "None":
    tag = None
author = "Ryan Fisher <ryan.fisher@ligo.org>"
builder = "Ryan Fisher <ryan.fisher@ligo.org>"
committer = "Ryan Fisher <ryan.fisher@ligo.org>"
status = "CLEAN: All modifications committed"
version = id
verbose_msg = """Branch: master
Tag: glue-release-1-55-1
Id: e53000c136f795ef247b0fea9e1ad92d17c563cd

Builder: Ryan Fisher <ryan.fisher@ligo.org>
Build date: 2017-04-07 16:25:53 +0000
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
    if foreign_id == "e53000c136f795ef247b0fea9e1ad92d17c563cd":
        return
    msg = "Program id (e53000c136f795ef247b0fea9e1ad92d17c563cd) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)

