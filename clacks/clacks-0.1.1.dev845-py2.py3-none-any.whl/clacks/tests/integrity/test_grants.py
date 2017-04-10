#!/usr/bin/env python3

"""Test if there are any mappers left in config."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from gtcms.core import cfg
from nose.tools import eq_


class TestGrants(object):

    """Test if there are any mappers left in config."""

    def test_system_grants(self):
        """Test if there are any mappers left in config."""

        from gtcms.models import Grant

        engine = create_engine('postgresql://%s:%s@%s:%d/%s' %
                               (cfg.get('db', 'user'),
                                cfg.get('db', 'password'),
                                cfg.get('db', 'host', default='localhost'),
                                cfg.get('db', 'port', default=5432),
                                cfg.get('db', 'database')[:-5]),
                               echo=False,
                               convert_unicode=True,)
        db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=True,
                                         autocommit=False))
        dbgrants = {g[0] for g
                    in db.execute('SELECT name FROM grants_dictionary').fetchall()
                    if g[0].isupper()}
        systemgrants = set(Grant.systemGrants().keys())
        # all systemgrants should be defined in database:
        eq_(systemgrants.difference(dbgrants), set())
        # and database ideally should contain only known system grants
        eq_(dbgrants.difference(systemgrants), set())


    def test_controls_required_grants(self):
        """Test if all grants required by controls are defined in database."""

        engine = create_engine('postgresql://%s:%s@%s:%d/%s' %
                               (cfg.get('db', 'user'),
                                cfg.get('db', 'password'),
                                cfg.get('db', 'host', default='localhost'),
                                cfg.get('db', 'port', default=5432),
                                cfg.get('db', 'database')[:-5]),
                               echo=False,
                               convert_unicode=True,)
        db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=True,
                                         autocommit=False))
        dbgrants = {g[0] for g
                    in db.execute('SELECT name FROM grants_dictionary').fetchall()
                    if g[0].isupper()}
        controlgrants = set(sum([a['grants'] for x, a in cfg.get('admin', 'scripts').items()
                                 if 'grants' in a], []))
        eq_(controlgrants.difference(dbgrants), set())
