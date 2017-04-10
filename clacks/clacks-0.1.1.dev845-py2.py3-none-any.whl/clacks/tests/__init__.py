#!/usr/bin/env python3

""" GtCMS tests package """

from gtcms.core import cfg

cfg.cacheFile = None
cfg.config['db']['echo'] = True
assert cfg.get('db', 'database')[-5:] == '_test'

from gtcms.core.db import db, create_all  # noqa


def newTestDB():

    """Create fresh reference database for safe testing."""

    from sqlalchemy import create_engine

    assert cfg.get('db', 'database')[-5:] == '_test'

    conn = create_engine('postgresql://%s:%s@%s:%d/%s' %
                         (cfg.get('db', 'user'),
                          cfg.get('db', 'password'),
                          cfg.get('db', 'host', default='localhost'),
                          cfg.get('db', 'port', default=5432),
                          'template1'),
                         echo=False,
                         convert_unicode=True).connect()
    conn.connection.set_isolation_level(0)
    conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='%s';" %
                 cfg.get('db', 'database'))
    conn.execute('DROP DATABASE IF EXISTS "%s";' % cfg.get('db', 'database'))
    conn.execute('CREATE DATABASE "%s" WITH '
                 "  ENCODING = 'UTF8' TEMPLATE=template0 LC_COLLATE='pl_PL.UTF-8' "
                 "  LC_CTYPE='pl_PL.UTF-8';" % cfg.get('db', 'database'))
    conn.close()

    if False and ('schema' in cfg.get('db')):
        conn = create_engine('postgresql://%s:%s@%s:%d/%s' %
                             (cfg.get('db', 'user'),
                              cfg.get('db', 'password'),
                              cfg.get('db', 'host', default='localhost'),
                              cfg.get('db', 'port', default=5432),
                              cfg.get('db', 'database')),
                             echo=False,
                             convert_unicode=True).connect()
        conn.connection.set_isolation_level(0)
        conn.execute('DROP SCHEMA IF EXISTS %s' % (cfg.get('db', 'schema'),))
        conn.execute('CREATE SCHEMA %s' % (cfg.get('db', 'schema'),))

newTestDB()
create_all()
db.commit()
