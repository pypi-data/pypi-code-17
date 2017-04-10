#!/usr/bin/env python3

"""Core module init script."""

import re
from datetime import date

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .core import ROOTPATH, cfg

db = None
engine = None


def set_search_path(db_conn, conn_proxy):  # pylint: disable=unused-argument
    """Set search path."""
    db_conn.cursor().execute('set search_path=public')


def __init_db():
    """Initialize global connections"""
    global db, engine  # pylint: disable=global-statement
    engine = create_engine('postgresql://%s:%s@%s:%d/%s' %
                           (cfg.get('db', 'user'),
                            cfg.get('db', 'password'),
                            cfg.get('db', 'host', default='localhost'),
                            cfg.get('db', 'port', default=5432),
                            cfg.get('db', 'database')),
                           echo=cfg.get('db', 'echo', default=False),
                           convert_unicode=True,)
    if db is None:
        db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=True,
                                         autocommit=False))
        db.meta = MetaData(bind=engine)
    else:
        meta = db.meta
        db.flush()
        db.commit()
        db.remove()
        db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=True,
                                         autocommit=False))
        db.meta = meta
        db.meta.bind = engine

__init_db()


def create_all():  # pylint: disable=too-many-branches

    """ Custom version of MetaData create_all that additionally imports
    stored procedures from well known location and is able to patch
    already created tables.
    """

    from gtcms.models import DbFeature

    emptydb = not db.execute("SELECT COUNT(tablename) FROM pg_tables "
                             "  WHERE tablename NOT LIKE 'pg_%' "
                             "    AND tablename NOT LIKE 'sql_%'").fetchone()[0]

    initdate, setinitdate = None, False

    if not emptydb:
        initdate = db.query(DbFeature).filter_by(name='init').first()

    if not initdate:
        initdate = DbFeature('init', date.today() if emptydb else date(2011, 11, 5))
        setinitdate = True

    if (ROOTPATH/'sql').is_dir():
        patches = sorted(a for a in (ROOTPATH/'sql').iterdir()
                         if re.match(r'^[0-9]+.*\.sql$', a.name))
    else:
        patches = []

    if not emptydb:
        # first loop goes through migration patches
        for patch in (p for p in patches if re.match(r'^[0-9]{8}-.*\.sql$', p.name)):
            patchname = patch.name[9:-4]
            dbfeature = db.query(DbFeature).filter(DbFeature.name == patchname).first()
            patchdate = date(int(patch.name[:4]), int(patch.name[4:6]), int(patch.name[6:8]))
            if initdate.applied < patchdate and (not dbfeature or dbfeature.applied < patchdate):
                with patch.open('r', encoding='utf-8') as phandle:
                    script = phandle.read()

                print(patch.name, patchname)
                if len(script):
                    for scline in re.split(';\n\n\n', script):
                        db.execute(scline)

                if dbfeature:
                    dbfeature.applied = patchdate
                else:
                    db.add(DbFeature(patchname, patchdate))
                db.commit()

    if not cfg.get('db', 'schema', default=None):
        db.meta.create_all()
    else:
        # workaround for not creating tables from PGSQL search_path
        existing = [t[0] for t in
                    db.execute("SELECT table_name FROM information_schema.tables"
                               "  WHERE table_schema='public' OR table_schema='%s'"
                               % (cfg.get('db', 'schema'),)).fetchall()]
        db.meta.create_all(tables=[v for k, v in db.meta.tables.items() if k not in existing])

    if setinitdate:
        db.add(initdate)

    db.commit()

    # second loop goes through feature patches
    for patch in patches:
        if re.match(r'^[0-9]{2}-.*\.sql$', patch.name):
            patchname = patch.name[3:-4]
            dbfeature = db.query(DbFeature).filter(DbFeature.name == patchname).first()
            if not dbfeature:
                script = patch.open('r', encoding='utf-8').read()
                try:
                    print(patch.name, patchname)
                    db.execute(script)
                except Exception as e:
                    print(repr(e))
                    raise e
                else:
                    db.add(DbFeature(patchname))
                    db.commit()
