#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 David Hoese
# Author(s):
#   David Hoese <david.hoese@ssec.wisc.edu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Utilities for testing.

This mostly takes from astropy's method for checking warnings during tests.
"""
import sys
import six
import types
import warnings


_deprecations_as_exceptions = False
_include_astropy_deprecations = False
AstropyDeprecationWarning = None
AstropyPendingDeprecationWarning = None


def treat_deprecations_as_exceptions():
    """
    Turn all DeprecationWarnings (which indicate deprecated uses of
    Python itself or Numpy, but not within Astropy, where we use our
    own deprecation warning class) into exceptions so that we find
    out about them early.

    This completely resets the warning filters and any "already seen"
    warning state.
    """
    # First, totally reset the warning state
    for module in list(six.itervalues(sys.modules)):
        # We don't want to deal with six.MovedModules, only "real"
        # modules.
        if (isinstance(module, types.ModuleType) and
            hasattr(module, '__warningregistry__')):
            del module.__warningregistry__

    if not _deprecations_as_exceptions:
        return

    warnings.resetwarnings()

    # Hide the next couple of DeprecationWarnings
    warnings.simplefilter('ignore', DeprecationWarning)
    # Here's the wrinkle: a couple of our third-party dependencies
    # (py.test and scipy) are still using deprecated features
    # themselves, and we'd like to ignore those.  Fortunately, those
    # show up only at import time, so if we import those things *now*,
    # before we turn the warnings into exceptions, we're golden.
    try:
        # A deprecated stdlib module used by py.test
        import compiler  # pylint: disable=W0611
    except ImportError:
        pass

    try:
        import scipy  # pylint: disable=W0611
    except ImportError:
        pass

    # Now, start over again with the warning filters
    warnings.resetwarnings()
    # Now, turn DeprecationWarnings into exceptions
    warnings.filterwarnings("error", ".*", DeprecationWarning)

    # Only turn astropy deprecation warnings into exceptions if requested
    if _include_astropy_deprecations:
        warnings.filterwarnings("error", ".*", AstropyDeprecationWarning)
        warnings.filterwarnings("error", ".*", AstropyPendingDeprecationWarning)

    if sys.version_info[:2] >= (3, 4):
        # py.test reads files with the 'U' flag, which is now
        # deprecated in Python 3.4.
        warnings.filterwarnings(
            "ignore",
            r"'U' mode is deprecated",
            DeprecationWarning)

        # BeautifulSoup4 triggers a DeprecationWarning in stdlib's
        # html module.x
        warnings.filterwarnings(
            "ignore",
            r"The strict argument and mode are deprecated\.",
            DeprecationWarning)
        warnings.filterwarnings(
            "ignore",
            r"The value of convert_charrefs will become True in 3\.5\. "
            r"You are encouraged to set the value explicitly\.",
            DeprecationWarning)

    if sys.version_info[:2] >= (3, 5):
        # py.test raises this warning on Python 3.5.
        # This can be removed when fixed in py.test.
        # See https://github.com/pytest-dev/pytest/pull/1009
        warnings.filterwarnings(
            "ignore",
            r"inspect\.getargspec\(\) is deprecated, use "
            r"inspect\.signature\(\) instead",
            DeprecationWarning)


class catch_warnings(warnings.catch_warnings):
    """
    A high-powered version of warnings.catch_warnings to use for testing
    and to make sure that there is no dependence on the order in which
    the tests are run.

    This completely blitzes any memory of any warnings that have
    appeared before so that all warnings will be caught and displayed.

    ``*args`` is a set of warning classes to collect.  If no arguments are
    provided, all warnings are collected.

    Use as follows::

        with catch_warnings(MyCustomWarning) as w:
            do.something.bad()
        assert len(w) > 0
    """
    def __init__(self, *classes):
        super(catch_warnings, self).__init__(record=True)
        self.classes = classes

    def __enter__(self):
        warning_list = super(catch_warnings, self).__enter__()
        treat_deprecations_as_exceptions()
        if len(self.classes) == 0:
            warnings.simplefilter('always')
        else:
            warnings.simplefilter('ignore')
            for cls in self.classes:
                warnings.simplefilter('always', cls)
        return warning_list

    def __exit__(self, type, value, traceback):
        treat_deprecations_as_exceptions()


