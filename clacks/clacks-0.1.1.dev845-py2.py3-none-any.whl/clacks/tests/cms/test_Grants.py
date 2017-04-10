#!/usr/bin/env python3

"""User class tests."""

from nose.tools import eq_


class TestGrants(object):

    """User class tests."""

    def setUp(self):
        """Begin temporary transaction"""
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """Rollback temporary transaction"""
        from gtcms.core.db import db
        db.rollback()


    def test_updateAll(self):
        """Test whether it is possible to nest grants"""
        from gtcms.core.db import db
        from gtcms.models import Grant
        Grant.updateAll()
        eq_(set(Grant.systemGrants().keys()),
            {g.name for g in db.query(Grant).all()})
