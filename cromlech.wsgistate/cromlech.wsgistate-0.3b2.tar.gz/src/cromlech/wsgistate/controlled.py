# -*- coding: utf-8 -*-
"""Wsgistate integration to the cromlech stack

The session is meant to be unique for the application. In the same way as zope
attach the site manager to current thread, session is attached to computing
thread by the application.

The session is automatically saved at end of context manager if no exceptions
occurs
"""

from cromlech.browser import setSession, getSession
from cromlech.browser.interfaces import ISession
from transaction.interfaces import IDataManagerSavepoint, IDataManager
from zope.interface import implementer

try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict


class SessionStateException(Exception):
    pass


class State(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<SessionState %r>' % self.name


CLEAN = State('clean')
UNSAVED = State('modified')
ABORTED = State('aborted')
CLOSED = State('closed')


@implementer(IDataManagerSavepoint)
class Savepoint(UserDict):

    def __init__(self, transactor, data):
        UserDict.__init__(self)
        self.transactor = transactor
        self.update(data)

    def rollback(self):
        self.transactor.data.clear()
        self.transactor.update(self.data)


@implementer(ISession, IDataManager)
class WsgistateDataManager(UserDict):

    save = None
    state = CLEAN

    def __init__(self, manager):
        self.manager = manager
        self._last_commit = self.canonical = manager.session
        self.data = manager.session.copy()

    def savepoint(self):
        if self.state is UNSAVED:
            self.save = Savepoint(self, self.data)
            self.state = CLEAN
        elif self.state in [ABORTED, CLOSED]:
            raise SessionStateException(
                "Session's current state disallows saving operations.")
        return self.save

    def __persist(self, data):
        self.manager.session = data

    def commit(self, transaction):
        self._last_commit = self.data.copy()
        self.__persist(self._last_commit)

    def __setitem__(self, name, value):
        if self.state not in [CLOSED, ABORTED]:
            self.state = UNSAVED
            UserDict.__setitem__(self, name, value)
        else:
            raise SessionStateException(
                "Session's current state disallows writing")

    def abort(self, transaction):
        if self.state not in [ABORTED, CLOSED]:
            self.clear()
            self.data = self._last_commit
            self.save = None
            self.state = ABORTED

    def tpc_begin(self, transaction):
        pass

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        self.state = CLOSED

    def tpc_abort(self, transaction):
        pass

    def sortKey(self):
        return "~cromlech.wsgisession"


class WsgistateSession(object):

    def __init__(self, environ, key, transaction_manager=None):
        self.manager = environ[key]
        self.transaction_manager = transaction_manager

    def __enter__(self):
        if self.transaction_manager is not None:
            dm = WsgistateDataManager(self.manager)
            self.transaction_manager.join(dm)
            setSession(dm)
            return dm
        else:
            setSession(self.manager.session)
            return self.manager.session

    def __exit__(self, type, value, traceback):
        setSession()
