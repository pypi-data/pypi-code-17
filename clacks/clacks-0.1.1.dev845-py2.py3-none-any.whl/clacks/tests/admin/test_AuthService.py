#!/usr/bin/env python3

"""Authorization service tests."""

from unittest.mock import MagicMock
from nose.tools import eq_

from gtcms.core.db import db
import gtcms.cptools.access_grants # pylint: disable=unused-import


class TestAdminAuth(object):

    """Authorization service tests."""

    def setUp(self):
        """Start temporary transaction"""

        from gtcms.models import User
        import cherrypy

        db.begin_nested()
        user = User()
        user.login = 'test'
        user.password = 'test'
        user.active = True
        db.add(user)
        db.flush()
        cherrypy.request.user = None


    def teardown(self):
        """Kill temporary transaction"""
        import cherrypy
        db.rollback()
        del cherrypy.request.user


    def test_remoteLogin_empty_super_password(self):
        """Test remote login with empty remote password."""

        from gtcms.handlers.SessionV1 import Session

        eq_(Session.remoteLogin('admin', 'gt:'), False)


    def test_remoteLogin_invalid_super_password(self):
        """Test remote login with invalid remote password."""

        from gtcms.handlers.SessionV1 import Session

        eq_(Session.remoteLogin('admin', 'gt:abcdefghij'), False)


    # needs to be implemented with some mockup
    #def test_remoteLogin_valid_super_password(self)
    #    """Test remote login with valid remote password."""
    #    eq_(AdminAuth.remoteLogin('admin', 'gt:really???'), True)


    def test_AdminAuth_status(self):
        """Check if AdminAuth.status() executes cleanly."""

        import cherrypy
        from gtcms.handlers.SessionV1 import Session

        cherrypy.session = MagicMock()
        auth = Session()
        auth.status()


    def test_bad_admin_login(self):
        """Check if AdminAuth.status() executes cleanly."""

        import cherrypy
        from gtcms.handlers.SessionV1 import Session

        cherrypy.session = MagicMock()
        auth = Session()
        response = auth.login(login="random", password="gt:")
        eq_(response, {'authorized': False})
