# -*- coding: utf-8 -*-

import tempfile
from wsgistate.session import SessionCache
from wsgistate.simple import session as session_decorator
from .timeout import TimeoutFileCache, TimeoutCookieSession


def file_session(path, **kw):
    def decorator(application):
        _file_base_cache = TimeoutFileCache(path, **kw)
        _file_session_cache = SessionCache(_file_base_cache, **kw)
        return TimeoutCookieSession(application, _file_session_cache, **kw)
    return decorator


def session_wrapper(app, *global_conf, **local_conf):
    session_key = local_conf.pop('session_key', 'session')
    wrapper = session_decorator(key=session_key, **local_conf)
    return wrapper(app)


def file_session_wrapper(app, *global_conf, **local_conf):
    session_key = local_conf.pop('session_key', 'session')
    path = local_conf.get('session_cache', tempfile.gettempdir())
    wrapper = file_session(path, key=session_key, **local_conf)
    return wrapper(app)
