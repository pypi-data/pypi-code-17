#!/usr/bin/env python3

"""Admin page generation test"""

from nose.tools import assert_in, assert_is_not_none    # pylint: disable=no-name-in-module
import gtcms.cptools.access_grants    # pylint: disable=unused-import



class TestAdminPage(object):

    """Admin page generation test"""

    def test_pageRenders(self):
        """Admin page generation test"""

        from gtcms.handlers.AdminPage import AdminPage

        page = AdminPage()
        result = page.index()
        assert_is_not_none(result)    #pylint: disable=no-value-for-parameter
        assert_in('dojo.js', result)    #pylint: disable=no-value-for-parameter
