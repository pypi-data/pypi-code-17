id = "73a7ac409185998c64181921ea1e573a72eaf311"
date = "2017-04-07 17:17:10 +0000"
branch = "master"
tag = "None"
if tag == "None":
    tag = None
author = "Ryan Fisher <ryan.fisher@ligo.org>"
builder = "Ryan Fisher <ryan.fisher@ligo.org>"
committer = "Ryan Fisher <ryan.fisher@ligo.org>"
status = "CLEAN: All modifications committed"
version = id
verbose_msg = """Branch: master
Tag: None
Id: 73a7ac409185998c64181921ea1e573a72eaf311

Builder: Ryan Fisher <ryan.fisher@ligo.org>
Build date: 2017-04-07 17:18:28 +0000
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
    if foreign_id == "73a7ac409185998c64181921ea1e573a72eaf311":
        return
    msg = "Program id (73a7ac409185998c64181921ea1e573a72eaf311) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)

