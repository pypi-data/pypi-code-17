#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext import declarative
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy_profile import sqlprofile


ENGINE = create_engine('sqlite:///')

Base = declarative.declarative_base()


class _User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


def assert_raises(exc):
    def _assert_raises(func):
        def __assert_raises(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exc:
                pass
            else:
                raise AssertionError('{0} did not raise')
        return __assert_raises
    return _assert_raises


class Test_sqlprofile(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(ENGINE)
        self.session_maker = sessionmaker(bind=ENGINE)

    def tearDown(self):
        Base.metadata.drop_all(ENGINE)

    @sqlprofile(ENGINE, count=1)
    def test_raw_execute(self):
        connection = ENGINE.connect()

        connection.execute('SELECT 1')

    @sqlprofile(ENGINE,
                count=4, insert=1, update=1, select=1, delete=1,
                seq='iusd')
    def test(self):
        session = self.session_maker()

        user = _User(name='Alice')

        # INSERT
        with session.begin(subtransactions=True):
            session.add(user)

        # UPDATE
        with session.begin(subtransactions=True):
            user.name = 'Bob'

        # SELECT
        session.query(_User).all()

        # DELETE
        with session.begin(subtransactions=True):
            session.delete(user)

    @assert_raises(AssertionError)
    @sqlprofile(ENGINE, count=0)
    def test_count_mismatch(self):
        session = self.session_maker()

        user = _User(name='Alice')

        # INSERT
        with session.begin(subtransactions=True):
            session.add(user)

    @assert_raises(AssertionError)
    @sqlprofile(ENGINE, seq='s')
    def test_seq_mismatch(self):
        session = self.session_maker()

        user = _User(name='Alice')

        # INSERT
        with session.begin(subtransactions=True):
            session.add(user)


if __name__ == '__main__':
    unittest.main()
