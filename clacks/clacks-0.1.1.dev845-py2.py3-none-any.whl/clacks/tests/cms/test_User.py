#!/usr/bin/env python3

"""User class tests."""

from nose.tools import eq_


class TestUser(object):

    """User class tests."""

    def setUp(self):
        """Begin temporary transaction"""
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """Rollback temporary transaction"""
        from gtcms.core.db import db
        db.rollback()


    def test_nested_grant(self):
        """Test whether it is possible to nest grants"""
        from gtcms.core.db import db
        from gtcms.models import Grant
        g1 = Grant(name='all_of_us')
        db.add(g1)
        db.flush()
        g2 = Grant(name='VIEW')
        g1.grants[g2.name] = g2
        db.flush()
        g2.grants[g1.name] = g1
        db.flush()
        eq_(set(db.query(Grant).all()), set((g1, g2)))


    def test_user_grants(self):
        """Verify if User.grants contain nested grants as well"""
        from gtcms.core.db import db
        from gtcms.models import User, Grant
        g1 = Grant(name='G1')
        g2 = Grant(name='G2')
        g1.grants['G2'] = g2
        db.add(g1)
        c = User(login='user')
        db.add(c)
        c.setGrant('G1')
        eq_(c.grants, {g.name for g in (g1, g2)})
        c.dropGrant('G1')
        eq_(c.grants, frozenset())


    def test_recursive_grants(self):
        """More recursion tests"""
        from gtcms.core.db import db
        from gtcms.models import User, Grant
        g1 = Grant(name='G1')
        g2 = Grant(name='G2')

        g11 = Grant(name='G1.1')
        g21 = Grant(name='G2.1')
        g22 = Grant(name='G2.2')
        db.add(g1)
        db.add(g2)
        db.add(g11)
        db.add(g21)
        db.add(g22)
        g1.grants.set(g11)
        g2.grants.set(g21)
        g2.grants.set(g22)
        c1 = User(login='user')
        c2 = User(login='user2')
        db.add(c1)
        db.add(c2)
        c1.setGrant('G1')
        eq_(c1.grants, {g.name for g in (g1, g11)})
        c2.setGrant('G2')
        c2.setGrant('G1.1')
        eq_(c2.grants, {g.name for g in (g2, g21, g22, g11)})
        c1.dropGrant('G1')
        eq_(c1.grants, frozenset())
        c2.dropGrant('G2')
        eq_(c2.grants, {g.name for g in (g11,)})


    def test_users(self):
        """Test if grant lists its users"""
        from gtcms.core.db import db
        from gtcms.models import User, Grant
        g1 = Grant(name='G1')
        g2 = Grant(name='G2')

        g11 = Grant(name='G1.1')
        g21 = Grant(name='G2.1')
        g22 = Grant(name='G2.2')
        db.add(g1)
        db.add(g2)
        db.add(g11)
        db.add(g21)
        db.add(g22)
        g1.grants.set(g11)
        g2.grants.set(g21)
        g2.grants.set(g22)
        c1 = User(login='user')
        c2 = User(login='user2')
        db.add(c1)
        db.add(c2)
        c1.setGrant('G1')
        eq_(g11.name in c1.grants, True)
        eq_(set(g11.users[:]), {c1})
        c2.setGrant('G2')
        c2.setGrant('G1.1')
        eq_(set(g11.users[:]), {c1, c2})
        c1.dropGrant('G1')
        eq_(set(g22.users[:]), {c2})
