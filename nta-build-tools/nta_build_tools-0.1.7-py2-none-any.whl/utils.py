# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2017, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""Utility functions."""

import collections
import subprocess



def subprocessCall(command, dryrun, checkCall=False, shell=True):
  """Execute command in a subprocess.

  :param command: the command to execute. E.g. `["ls", "-l"]`
  :param dryrun: Boolean. If true, print command without executing it.
  :param checkCall: if true, raise exception on non-zero exit code
  :param shell: boolean whether to run command in a shell
  """
  assert (not isinstance(command, str) and
          isinstance(command, collections.Sequence))
  if dryrun:
    print "Would execute: {}".format(" ".join(command))
  else:
    print "Executing: {}".format(" ".join(command))
    command = " ".join(command)
    if checkCall:
      return subprocess.check_call(command, shell=shell)
    else:
      return subprocess.call(command, shell=shell)
