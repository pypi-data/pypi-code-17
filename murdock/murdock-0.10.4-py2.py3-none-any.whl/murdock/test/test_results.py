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

"""A set of `pytest` routines for `.results` module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

import murdock.results


class TestTimingDict(object):

    TDICTS =  (
        murdock.results.TimingDict(**{'process': None, 'wall': None}),
        murdock.results.TimingDict(**{'process': 1.337, 'wall': None}),
        murdock.results.TimingDict(**{'process': None, 'wall': 13.37}),
        murdock.results.TimingDict(**{'process': 1.337, 'wall': 13.37})
        )

    @pytest.mark.parametrize(
        'test_input,expected', (
            (TDICTS[0], False),
            (TDICTS[1], False),
            (TDICTS[2], False),
            (TDICTS[3], True)
            ))
    def test_bool(self, test_input, expected):
        assert bool(test_input) is expected
