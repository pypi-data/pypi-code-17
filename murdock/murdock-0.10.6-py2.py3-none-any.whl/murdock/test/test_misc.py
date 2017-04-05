# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""A set of `pytest` routines for the `.misc` module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest

import murdock.misc


def test_create_filelink():
    outdir = '.'
    targetpath = 'test_create_filelink_trg.tmp'
    linkname = 'test_create_filelink_lnk.tmp'
    if os.path.exists(targetpath) or os.path.exists(linkname):
        raise Exception(
            'Remove files `%s` and `%s` to run test.' % (targetpath, linkname))
    with open(targetpath, 'w') as f:
        f.write('')
    assert murdock.misc.create_filelink(outdir, targetpath, linkname)
    os.remove(targetpath)
    if os.path.lexists(linkname):
        os.remove(linkname)
