# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Content provider'''

import os
import multiprocessing as mp
import contextlib
import functools
import collections
from enum import Enum

from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm.attributes import set_committed_value

import feedcommas.config as config
import feedcommas.client as client
import feedcommas.model as model
from feedcommas.utils import get_password_cmd, now_ts, UNUSED
from feedcommas.log import log
from feedcommas.locale import _


@contextlib.contextmanager
def make_provider(*args, **kwargs):
    '''Context Manager for `Provider` class'''
    p = Provider(*args, **kwargs)
    try:
        yield p
    finally:
        p.stop()


class ReadType(Enum):
    '''Specificator used for filtering articles marked as read, unread or any of
    them.

    Note:
      ReadType.READ is only supported in offline mode (Comma Feed doesn't allow
      to request only read entries).'''
    ALL = 'all'
    READ = 'read'
    UNREAD = 'unread'

    @staticmethod
    def current():
        '''Returns a current config setting casted to a correct enum values.'''
        read = config.get_value('settings.show-read')
        return ReadType.ALL if read else ReadType.UNREAD


class LocalResult:
    '''Implements multiprocessing.pool.AsyncResult interface. It's an object
    returned by local database calls.

    Additionally, when constructed, can call a given callback.'''
    def __init__(self, retval=None, callback=None):
        self.retval = retval
        if callback is not None:
            callback(self.retval)

    def get(self, *a, **kw):  # pylint: disable=missing-docstring
        return self.retval

    def wait(self, *a, **kw):  # pylint: disable=missing-docstring
        return

    def ready(self, *a, **kw):  # pylint: disable=missing-docstring
        return True

    def successful(self, *a, **kw):  # pylint: disable=missing-docstring
        return True


class _RequestStatus:
    '''Wrapper for status of network request. Its state tells whether there was
    an error when trying to reach a remote server and if it's feasible to check
    it again.'''
    _failed = False
    _fail_ts = 0
    _delay = 8

    def __init__(self):
        self.reset()

    def should_check(self):
        '''Tells whether it's feasible to use a network again.'''
        return (self._failed is False or
                now_ts() - self._fail_ts > self._delay)

    def fail(self):
        '''Indicate a failure in last network request.'''
        # exponential backoff
        next_delay = self._delay * 2
        if self._failed is True and self.should_check() and next_delay < 900:
            self._delay = next_delay

        self._failed = True
        self._fail_ts = now_ts()

    def reset(self):
        '''Reset request status to initial value (no failure).'''
        self._failed = _RequestStatus._failed
        self._fail_ts = _RequestStatus._fail_ts
        self._delay = _RequestStatus._delay


class _OnlineAware:
    def __init__(self, online_f, offline_f=None):
        self._online_f = online_f
        self._offline_f = offline_f

    def __get__(self, obj, objtype=None):
        retf = None
        if self._offline_f is None:
            retf = self._online_f
        elif obj.online():
            retf = self._online_f
        else:
            retf = self._offline_f
        return functools.partial(retf, obj)


class Provider:
    '''Asynchrounous content provider. Dispatches jobs of fetching data from
    commafeed to the pool of workers and calls given callbacks with fetched
    data. Also communicates with urwid's main loop to update it after calling a
    callback for each request.'''

    class _MultipleCallbacks:
        '''Thanks to this class we avoid a need to call a callback from
        callback - it decouples callbacks logic and assures us that one callback
        won't modify the other's input'''
        def __init__(self, *callbacks):
            self._callbacks = list(callbacks)

        def __call__(self, *args, **kwargs):
            for cb in self._callbacks:
                if callable(cb):
                    cb(*args, **kwargs)

    def __init__(self, urwid_loop):
        self._req_status = _RequestStatus()

        self._notify_pipe = urwid_loop.watch_pipe(lambda _: True)

        self._username = config.get_value('server.username')
        pass_cmd = config.get_value('server.password-cmd')
        if pass_cmd:
            ok, self._password, err = get_password_cmd(pass_cmd)
            if not ok:
                log.error(err)
                self._password = config.get_value('server.password')
        else:
            self._password = config.get_value('server.password')

        self._pool = None
        self._start_pool()

    def online(self):
        '''Returns whether Provider is currently in online mode (i.e. whether
        requests result in database or CommaFeed query.

        Provider can automatically switch to offline mode for some time when
        requests fail due to network error. It will then repeatedly try to go
        back to online mode.'''
        cfg_offline = config.get_value('settings.offline')
        if cfg_offline:
            return False
        return self._req_status.should_check()

    def change_credentials(self, username, password, verify=False):
        '''Changes login credentials used for HTTP Simple auth. Credentials are
        verified to be correct: Provider tries to connect with them first. If
        they're correct, they're changed and all new requests will be made using
        them.

        This function doesn't save new credentials to config, because it doesn't
        know the origin of password ('password' or 'password-cmd' option).

        This function blocks until verification is done.'''
        try:
            correct = self._call(client.login, username, password)
        except client.APIFailure:
            correct = False

        if correct is True:
            self._username = username
            self._password = password
            self._start_pool()
        return correct

    def stop(self):
        '''Stops the service: workers are forcefully terminated and
        notifications to urwid are stopped.'''
        self._pool.terminate()
        os.close(self._notify_pipe)

    def reset_network_error(self):
        '''Resets errors occured when communicating with Comma Feed. This resets
        all counters and timeouts.'''
        self._req_status.reset()

    def _get_articles_db(self, type_, feed_id, read_type, limit=20, offset=0,
                         callback=None):
        UNUSED(type_)

        with model.make_session() as session:
            meta = self._query(session, feed_id, read_type, limit, offset)
            return LocalResult(meta, callback)

    def _get_articles_cf(self, type_, feed_id, read_type, limit=20, offset=0,
                         callback=None):
        assert read_type in (ReadType.ALL, ReadType.UNREAD)

        cb = self._MultipleCallbacks(self._update_articles, callback)

        def _db_fallback():
            self._get_articles_db(type_, feed_id, read_type, limit, offset,
                                  callback)

        return self._async_call(client.get_articles,
                                cb=cb, error_cb=_db_fallback,
                                type_=type_, id=feed_id,
                                readType=read_type.value,
                                limit=limit, offset=offset)

    def _get_feeds_db(self, callback=None):
        with model.make_session() as session:
            # We need all feeds anyway - we'll eager load all of them and
            # manually set parent-children relationship without dirtying the
            # session (via set_committed_value).
            #
            # See: http://stackoverflow.com/a/5701523/1088577
            nodes = session.query(model.Feed).all()
            children = collections.defaultdict(list)

            for node in nodes:
                if node.parent:
                    children[node.parent.id].append(node)

            root = None
            for node in nodes:
                set_committed_value(node, 'children', children[node.id])
                if node.id == 'all':
                    root = node

            if root is None:
                log.error(_('No feeds for offline reading'))
            return LocalResult(root, callback)

    def _get_feeds_cf(self, callback=None):
        cb = self._MultipleCallbacks(self._update_feeds, callback)

        def _db_fallback():
            self._get_feeds_db(callback)

        return self._async_call(client.get_feeds, cb, error_cb=_db_fallback)

    def _mark_db(self, entry_id, as_read):
        with model.make_session() as session:
            article = session.query(model.Article) \
                             .filter(model.Article.id == entry_id) \
                             .filter(model.Article.markable.is_(True)) \
                             .first()

            if article:
                article.read = as_read
                session.add(article)

                feed = session.query(model.Feed) \
                              .filter(model.Feed.id == article.feed_id) \
                              .first()

                if feed:
                    if as_read is True:
                        feed.unread = max(0, feed.unread - 1)
                    else:
                        feed.unread = max(0, feed.unread + 1)
                    session.add(feed)

    def _mark_cf(self, entry_id, as_read):
        self._mark_db(entry_id, as_read)
        self._async_call(client.mark, type_='entry', id=entry_id, read=as_read)

    def _mark_all_read_db(self, req_feed):
        with model.make_session() as session:
            meta = self._query(session, req_feed.id, ReadType.UNREAD)

            for article in meta.articles:
                article.read = not article.read

            session.add_all(meta.articles)

            node = session.query(model.Feed) \
                          .filter(model.Feed.id == req_feed.id) \
                          .first()

            for feed in node.dfs():
                feed.unread = 0
                session.add(feed)

    def _mark_all_read_cf(self, req_feed):
        self._mark_all_read_db(req_feed)

        req_type = 'category' if req_feed.is_category else 'feed'
        self._async_call(client.mark, type_=req_type, id=req_feed.id)

    def _star_db(self, entry_id, feed_id, starred):
        with model.make_session() as session:
            session.query(model.Article) \
                   .filter(model.Article.id == entry_id) \
                   .update({'starred': starred})

    def _star_cf(self, entry_id, feed_id, starred):
        self._star_db(entry_id, feed_id, starred)
        self._async_call(client.star, id=entry_id, feedId=feed_id,
                         starred=starred)

    def _update_articles(self, meta):
        self._req_status.reset()
        with model.make_session() as session:
            for article in meta.articles:
                session.merge(article)

    def _update_feeds(self, root):
        self._req_status.reset()
        with model.make_session() as session:
            session.query(model.Feed).delete()
        with model.make_session() as session:
            session.add(root)

    def _query(self, session, feed_id, read_type=ReadType.ALL,
               limit=None, offset=None):
        node = session.query(model.Feed) \
                      .options(joinedload_all('*')) \
                      .filter(model.Feed.id == feed_id) \
                      .first()

        if node is None:
            return []

        feed_ids = [feed.id for feed in node.bfs()]

        if feed_ids == ['starred']:
            query = session.query(model.Article) \
                           .filter(model.Article.starred.is_(True))
        else:
            query = session.query(model.Article) \
                           .filter(model.Article.feed_id.in_(feed_ids))

        if read_type == ReadType.UNREAD:
            query = query.filter(model.Article.read.is_(False))
        elif read_type == ReadType.READ:
            query = query.filter(model.Article.read.is_(True))

        query = query.order_by(model.Article.publish_date.desc())

        meta = client.ArticleMeta()
        meta.has_more = False

        if limit is not None:
            has_more_query = query.limit(1).offset(limit).exists()
            meta.has_more = session.query(has_more_query).scalar()
            query = query.limit(limit).offset(offset)

        if offset is not None:
            query = query.offset(offset)

        meta.articles = query.all()
        return meta

    def _start_pool(self):
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None

        workers_no = config.get_value('settings.workers')
        self._pool = mp.Pool(processes=workers_no,
                             initializer=client.init,
                             initargs=(self._username, self._password))

    def _async_call(self, fn, cb=None, error_cb=None, **kwargs):
        if cb is None:
            cb = lambda *a: True
        if error_cb is None:
            error_cb = lambda *a: True

        cb = functools.partial(self._cb, real_callback=cb)
        err_cb = functools.partial(self._err_cb, real_callback=error_cb)
        return self._pool.apply_async(fn, (), kwargs,
                                      callback=cb, error_callback=err_cb)

    def _call(self, fn, *args, **kwargs):
        return self._pool.apply(fn, args, kwargs)

    def _cb(self, data, real_callback):
        real_callback(data)
        os.write(self._notify_pipe, b'1')

    def _err_cb(self, exc, real_callback):
        # TODO FIXME: check type of error (only network ones should fail
        #             _req_status)
        self._req_status.fail()
        log.error(str(exc))
        real_callback()
        os.write(self._notify_pipe, b'1')

    # The Actual Interface (TM)
    get_articles = _OnlineAware(_get_articles_cf, _get_articles_db)
    get_feeds = _OnlineAware(_get_feeds_cf, _get_feeds_db)
    mark = _OnlineAware(_mark_cf, _mark_db)
    mark_all_read = _OnlineAware(_mark_all_read_cf, _mark_all_read_db)
    star = _OnlineAware(_star_cf, _star_db)
