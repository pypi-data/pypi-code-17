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

from ntabuildtools.repos import DEFAULT_REPOS, DEFAULT_ORDER



def executeInstall(repo, version, dryrun):
  if repo not in DEFAULT_REPOS:
    print "Unknown repository. This script currently supports: {}".format(DEFAULT_REPOS.keys())

  repoDir = os.path.expanduser("~/nta/{}".format(repo))
  package = DEFAULT_REPOS[repo]

  # Clean uninstall any currently installed version
  fullUninstall(repo, dryrun)

  # Install the package
  if version:
    subprocessCall(["ARCHFLAGS='-arch x86_64'", "pip", "install",
                    "{}=={}".format(package, version)],
                   dryrun, checkCall=True)
  else:
    os.chdir(repoDir)
    subprocessCall(["ARCHFLAGS='-arch x86_64'", "pip", "install",
                    "-e", "."],
                   dryrun, checkCall=True)



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("repos", metavar="repo", nargs="+", default=None,
                      help="One or more of: {}".format(
                          ",".join(DEFAULT_ORDER + ["all"])))
  parser.add_argument("--version", dest="version", default=None,
                      help="optional release version to install")
  parser.add_argument("--dryrun", action="store_true")
  parser.set_defaults(dryrun=False)

  args = parser.parse_args()

  if "all" in args.repos:
    repos = DEFAULT_ORDER
  else:
    repos = args.repos

  for repo in repos:
    executeInstall(repo, args.version, args.dryrun)
