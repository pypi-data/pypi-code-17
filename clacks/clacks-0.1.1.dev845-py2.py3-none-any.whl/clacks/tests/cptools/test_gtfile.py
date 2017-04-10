#!/usr/bin/env python3

""" gtfile unit tests """

import os

from nose.tools import eq_, assert_raises
from gtcms.cptools.gtfile import GtfileSession
from gtcms.core import fullPath

testpath = fullPath('caches/tests')
testfile = os.path.join(testpath, 'test')


class TestCmsTools(object):

    """ gtfile unit tests """

    @classmethod
    def setUpClass(cls):
        """ setUp """
        if os.path.isfile(testfile+'.lock'):
            os.unlink(testfile+'.lock')


    def test_lock_unlock(self):
        """ explicit locking and unlocking test """
        fses = GtfileSession(storage_path=testpath)
        fses.acquire_lock(testfile)
        fses.release_lock(testfile)


    def test_nested_acquire_release(self):
        """ nested locking and unlocking shouldn't cause breakages """
        fses = GtfileSession(storage_path=testpath)
        fses.acquire_lock()
        fses.acquire_lock()
        fses.release_lock()
        fses.release_lock()


    def test_nested_acquire_too_many_releases(self):
        """ session needs to be unlocked the same number of times as
        being locked in nested cases"""
        fses = GtfileSession(storage_path=testpath)
        fses.acquire_lock()
        fses.release_lock()
        assert_raises(KeyError, fses.release_lock)


    def test_with_session(self):
        """ session provides 'with' wrapper """
        fses = GtfileSession(storage_path=testpath)
        with fses.open(testfile) as lses:
            eq_(lses, fses)


    def test_with_session_nested(self):
        """ session provides 'with' wrapper that can be nested """
        fses = GtfileSession(storage_path=testpath)
        with fses.open(testfile) as lses:
            with lses.open(testfile) as nses:
                eq_(lses, fses)
                eq_(lses, nses)
