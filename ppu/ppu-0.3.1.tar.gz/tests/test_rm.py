#! /usr/bin/env python

import os
import subprocess
import sys
from ppu_tu import setup, teardown, find_in_path  # noqa
from ppu_tu import create_files, assert_files_exist, assert_files_not_exist


tmp_dir = None

test_prog_path = find_in_path('rm.py')
if not test_prog_path:
    sys.exit("Cannot find rm.py in %s" % os.environ["PATH"])


def test_rm():
    create_files(['test1', 'test2'])
    assert_files_exist(['test1', 'test2'])
    assert subprocess.call(
        [sys.executable, test_prog_path, "test2"]) == 0
    assert_files_exist('test1')
    assert_files_not_exist('test2')
