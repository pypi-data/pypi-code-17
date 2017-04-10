#!/usr/bin/env python3

"""Tests now obsolete core.env functions and constants."""

import os.path

import pytest

from gtcms.core import ROOTPATH, fullPath


class TestControls(object):

    """Tests now obsolete core.env functions and constants."""

    def test_fullPath_to_self(self):
        """Check if path to current file is resolved by fullPath()."""

        assert (fullPath('lib/gtcms/tests/core/test_core.py') ==
                os.path.abspath(__file__))

    def test_fullPath_to_project_ROOTPATH(self):
        """Test if fullpath on '.' or '' resolves to ROOTPATH"""
        assert fullPath('') == str(ROOTPATH)
        assert fullPath('.') == str(ROOTPATH)

    def test_fullPath_exception(self):
        """exception if path goes out of project"""
        with pytest.raises(ValueError):
            fullPath('..')
