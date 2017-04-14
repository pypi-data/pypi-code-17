# -*- coding: utf-8 -*-

"""
takumi_sqlalchemy.database
~~~~~~~~~~~~~~~~~~~~~~~~~~

Simplify database operations by using one single object under Takumi app.
"""

import threading
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.util import safe_reraise
from takumi_config import config
from takumi import define_hook

from .routing import RoutingSession
from .utils import normalize_dsn


def _create_engines(conf):
    dsn = normalize_dsn(conf['dsn'])

    def _s(x, d):
        return config.settings.get(x, d)
    max_overflow = conf.get('max_overflow', _s('DB_MAX_OVERFLOW', None))
    pool_size = conf.get('pool_size', _s('DB_POOL_SIZE', 10))
    kwargs = {
        'pool_recycle': conf.get('pool_recycle', _s('DB_POOL_RECYCLE', 1200))
    }
    if max_overflow is not None:
        kwargs['max_overflow'] = max_overflow
    if pool_size >= 0:
        kwargs['pool_size'] = pool_size

    return {r: create_engine(d, **kwargs) for r, d in dsn.items()}


def _create_sessions(engines):
    m = {}
    for app, e in engines.items():
        m[app] = scoped_session(sessionmaker(
            class_=RoutingSession,
            engines=e,
            expire_on_commit=False
        ))
    return m


class _NoneBinding(object):
    pass


class _DBContext(object):
    def __init__(self, session, data_entry):
        self._data_entry = data_entry
        self._session = session()
        self._data_entry.tags = {}
        self._binding = _NoneBinding

    def using_bind(self, name):
        # Remeber session binding
        if self._binding is _NoneBinding:
            self._binding = self._session._name
        self._session.using_bind(name)
        return self

    def tag(self, **kwargs):
        self._data_entry.tags.update(kwargs)
        return self

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._data_entry.tags.clear()
        session = self._session
        try:
            if session.transaction is None:
                return

            if exc_type is None:
                try:
                    session.commit()
                except:
                    with safe_reraise():
                        session.rollback()
            else:
                session.rollback()
        finally:
            try:
                session.close()
            finally:
                # Restore binding
                if self._binding is not _NoneBinding:
                    session._name = self._binding
                    self._binding = _NoneBinding


class _Database(object):
    """Convenient class for representing db sessions.

    A Database instance can have multiple sessions pointed to difference
    databases.

    :Example:

    >>> with db['takumi_demo'] as session:
    >>>...  session.query()
    """
    def __init__(self):
        self.__session_map = None
        # Store `app_ctx` and `tags`
        self._shared = threading.local()

        # engines = {
        #     'db1': {
        #         'master': Engine,
        #         'slave1': Engine,
        #         'slave2': Engine,
        #     }
        # }
        self._engines = {}
        settings = config.settings['DB_SETTINGS']
        # Eagerly create engine map
        for app_name, conf in settings.items():
            self._engines[app_name] = _create_engines(conf)

    def __getitem__(self, attr):
        if self.__session_map is None:
            # Create session map
            self.__session_map = _create_sessions(self._engines)
        return _DBContext(self.__session_map[attr], self._shared)

    def invalidate(self):
        """Invalidate all session connections
        """
        if not self.__session_map:
            return

        for session in self.__session_map.values():
            if session.registry.has():
                session.registry().invalidate()
            session.remove()

# This object is coroutine safe.
db = _Database()


# For sql comment
def _before_cursor_execute(conn, cursor, statement, params, context,
                           executemany):
    app_ctx = getattr(db._shared, 'app_ctx', {})
    tags = getattr(db._shared, 'tags', {})

    api_name = app_ctx.get('api_name', '-')
    request_id = app_ctx.get('request_id', '-')
    tags = ['{}={}'.format(k, v) for k, v in tags.items()]
    tags.sort()
    tags = ','.join(tags)
    statement = '/*[{}/{}]{}*/{}'.format(api_name, request_id, tags, statement)
    return statement, params


def _attach_events(db):
    for engines in db._engines.values():
        for engine in engines.values():
            event.listen(engine, 'before_cursor_execute',
                         _before_cursor_execute, retval=True)

_attach_events(db)


@define_hook(event='api_timeout')
def _timeout_hook(ctx):
    # Invalidate all in use session connections
    db.invalidate()


@define_hook(event='before_api_call')
def _db_ctx(ctx):
    db._shared._app_ctx = ctx


def _init_app(app):
    app.use(_timeout_hook)
    app.use(_db_ctx)

# Only `db` has the method `init_app`
db.init_app = _init_app
del _init_app
