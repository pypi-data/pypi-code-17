#!/usr/bin/env python3

"""Test if there are any mappers left in config."""

from gtcms.core import cfg
from nose.tools import eq_


class TestOldMappers(object):

    """Test if there are any mappers left in config."""

    def test_controls_migration(self):
        """Test if there are any mappers left in config."""

        eq_(cfg.get('mappers', default={}).keys(), {}.keys())
