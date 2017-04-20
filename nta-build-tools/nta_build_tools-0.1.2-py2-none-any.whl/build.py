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

import argparse
import os

from ntabuildtools.repos import HAS_CPP
from ntabuildtools.utils import subprocessCall



def executeBuild(repo, debug, debug_command, release_command,
                 make_command, install_command, dryrun):
  repoDir = os.path.expanduser("~/nta/{}".format(repo))

  if debug_command:
    debugDir = os.path.join(repoDir, "build", "scripts_debug")
    try:
      os.makedirs(debugDir)
    except OSError:
      pass

    print "Changing dir:", debugDir
    os.chdir(debugDir)

    # Execute the build
    subprocessCall(debug_command, dryrun, checkCall=True)
    subprocessCall(make_command, dryrun, checkCall=True)

    if debug:
      # Install debug build
      subprocessCall(install_command, dryrun, checkCall=True)

  if release_command:
    releaseDir = os.path.join(repoDir, "build", "scripts_release")
    try:
      os.makedirs(releaseDir)
    except OSError:
      pass

    print "Changing dir:", releaseDir
    os.chdir(releaseDir)

    subprocessCall(release_command, dryrun, checkCall=True)
    subprocessCall(make_command, dryrun, checkCall=True)

    if not debug:
      # Install release build
      subprocessCall(install_command, dryrun, checkCall=True)



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("repos", metavar="repo", nargs="+", default=None,
                      help="One or more of: {}".format(
                          ",".join(HAS_CPP + ["all"])))
  parser.add_argument("-d", dest="debug", action="store_true",
                      help="install the debug build")
  parser.add_argument("-r", dest="debug", action="store_false",
                      help="install the release build")
  parser.add_argument("--build-both", dest="build_both", action="store_true",
                      help="build both debug and release")
  parser.add_argument("--verbose", action="store_true")
  parser.add_argument("--dryrun", action="store_true")
  parser.add_argument("-j", type=int, default=6,
                      help="number of make jobs to run in parallel")
  parser.set_defaults(debug=False, build_both=False, dryrun=False)

  args = parser.parse_args()

  cmake_command = []
  if args.verbose:
    cmake_command.append("VERBOSE=1")

  cmake_command.extend([
    "cmake",
    "../..",
    "-DPY_EXTENSIONS_DIR=../../bindings/py/nupic/bindings",
  ])

  if "all" in args.repos:
    repos = HAS_CPP
  else:
    repos = args.repos

  if args.build_both or args.debug:
    debug_command = list(cmake_command)
    debug_command.extend([
      "-DCMAKE_INSTALL_PREFIX=../debug",
      "-DCMAKE_BUILD_TYPE=Debug",
      "-DNUPIC_IWYU=OFF",
    ])
  else:
    debug_command = None

  if args.build_both or not args.debug:
    release_command = list(cmake_command)
    release_command.extend([
      "-DCMAKE_INSTALL_PREFIX=../release",
      "-DCMAKE_BUILD_TYPE=Release",
      "-DNUPIC_IWYU=OFF",
    ])
  else:
    release_command = None

  make_command = ["make", "-j" + str(args.j)]
  install_command = ["make", "install"]

  for repo in repos:
    executeBuild(repo, args.debug, debug_command, release_command, make_command, install_command, args.dryrun)
