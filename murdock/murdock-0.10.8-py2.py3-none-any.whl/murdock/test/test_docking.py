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

"""A set of `pytest` routines for the `.runner.docking` module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import shutil

import pytest

from murdock import __path__ as MURDOCK_PATH
from murdock.logger import Logger


from murdock.runner.docking import Docking, DockingStep
import murdock.search.ps
import murdock.scoring.custom


INPUT_PATH = os.path.join(MURDOCK_PATH[0], 'test', 'input')

DOCKING_STEPS = [
    DockingStep(
        search_module='murdock.search.ps',
        search_parms={},
        scoring_module='murdock.scoring.custom',
        scoring_parms={'terms': []},
        transform_parms={}
    )
]
MOLDATA = {
    'label': 'docking_test_system',
    'receptor': {
        'label': 'receptor1',
        'filepath': os.path.join(INPUT_PATH, 'receptor1.mol2')
    },
    'ligands': [
        {
            'label': 'ligand1',
            'filepath': os.path.join(INPUT_PATH, 'ligand1.mol2')
        }
    ]
}



class TestDocking(object):


    def test_run_minimal(self):
        resdir = os.path.join('.', 'test_docking_tmp')
        if os.path.exists(resdir):
            print('Remove directory `%s` to run test `%s`.' % (resdir, type(self).__name__))
            assert False
        runner = murdock.runner.docking.Docking(
            label='test_docking', title='Test Docking', moldata=MOLDATA,
            docking_steps=DOCKING_STEPS, dry=True, resdir=resdir)
        try:
            assert runner.run()
        finally:
            logging.shutdown()
            logging.getLogger('murdock').handlers = []
            shutil.rmtree(resdir)
