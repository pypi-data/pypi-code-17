id = "b7816bfd696ff4713301d01f90897ca827d52c79"
date = "2017-05-04 21:30:39 +0000"
branch = "None"
tag = "glue-release-1.56.0"
if tag == "None":
    tag = None
author = "Ryan Fisher <ryan.fisher@ligo.org>"
builder = "Ryan Fisher <ryan.fisher@ligo.org>"
committer = "Ryan Fisher <ryan.fisher@ligo.org>"
status = "CLEAN: All modifications committed"
version = id
verbose_msg = """Branch: None
Tag: glue-release-1.56.0
Id: b7816bfd696ff4713301d01f90897ca827d52c79

Builder: Ryan Fisher <ryan.fisher@ligo.org>
Build date: 2017-05-04 21:34:47 +0000
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
    if foreign_id == "b7816bfd696ff4713301d01f90897ca827d52c79":
        return
    msg = "Program id (b7816bfd696ff4713301d01f90897ca827d52c79) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)

