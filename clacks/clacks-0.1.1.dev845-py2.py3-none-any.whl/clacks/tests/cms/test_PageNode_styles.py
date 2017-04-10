#!/usr/bin/env python3

"""Styles test"""

import os.path
from nose.tools import eq_

class TestSiteNode(object):

    """Styles test"""

    def setUp(self):
        """Temporary transaction started and styles path switched."""
        from gtcms.core.db import db
        from gtcms.models import PageNode
        db.begin_nested()
        self._oldStylesPath = PageNode._stylesPath
        PageNode._stylesPath = os.path.join(os.path.dirname(__file__), 'test-styles')
        PageNode._styles = {}


    def teardown(self):
        """Temporary transaction killed and styles path restored."""
        from gtcms.core.db import db
        from gtcms.models import PageNode
        db.rollback()
        PageNode._stylesPath = self._oldStylesPath
        PageNode._styles = {}


    def test_PageNode_fetch_styles(self):

        """Create basic page and validate its available styles."""

        from gtcms.tools import add_language

        page = add_language('pl', 'PL')[0]
        eq_(set(page.styles().keys()), set(['second', 'first']))
