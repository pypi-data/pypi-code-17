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

"""Info about the repos that this package manages."""
import os

DEFAULT_REPOS = {
  "nupic.core": "nupic.bindings",
  "nupic": "nupic",
  "htmresearch-core": "htmresearch_core",
  "htmresearch": "htmresearch",
}
DEFAULT_ORDER = ["nupic.core", "nupic", "htmresearch-core", "htmresearch"]

IMPORT_TEST = {
  "nupic.core": "nupic.bindings",
  "nupic": "nupic.algorithms",
  "htmresearch-core": "htmresearch_core",
  "htmresearch": "htmresearch",
}

IMPORT_PATH = {
  "nupic.core": os.path.expanduser("~/nta/nupic.core/bindings/py"),
  "nupic": os.path.expanduser("~/nta/nupic/src"),
  "htmresearch-core": os.path.expanduser("~/nta/htmresearch-core/bindings/py"),
  "htmresearch": os.path.expanduser("~/nta/htmresearch"),
}

REQUIREMENTS = {
  "nupic.core": os.path.expanduser(
      "~/nta/nupic.core/bindings/py/requirements.txt"),
  "nupic": os.path.expanduser("~/nta/nupic/requirements.txt"),
  "htmresearch-core": os.path.expanduser("~/nta/htmresearch-core/bindings/py/requirements.txt"),
  "htmresearch": os.path.expanduser("~/nta/htmresearch/requirements.txt"),
}

HAS_CPP = ["nupic.core", "htmresearch-core"]
CPP_EXTENSIONS_PATH = {
  "nupic.core": os.path.expanduser("~/nta/nupic.core/bindings/py/src/nupic/bindings"),
  "htmresearch-core": os.path.expanduser("~/nta/htmresearch-core/bindings/py/htmresearch_core"),
}
