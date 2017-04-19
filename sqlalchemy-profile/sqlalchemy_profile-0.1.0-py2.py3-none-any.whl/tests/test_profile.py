#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


from sqlalchemy.ext import declarative
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy_profile import StatementProfiler


Base = declarative.declarative_base()


class _User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Test_StatementProfiler(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_raw_execute(self):
        connection = self.engine.connect()

        profiler = StatementProfiler(self.engine)
        with profiler:
            connection.execute('SELECT 1')
            connection.execute('SELECT 2')

        assert profiler.count == 2

    def test_count(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        with profiler, session.begin(subtransactions=True):
            session.add(_User(name='Alice'))
            session.query(_User).all()

        assert profiler.count == 2
        assert profiler.insert == 1
        assert profiler.select == 1

    def test_clear(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        with profiler, session.begin(subtransactions=True):
            session.add(_User(name='Alice'))

        assert profiler.count == 1
        assert profiler.insert == 1

        profiler.clear()

        assert profiler.count == 0
        assert profiler.insert == 0

        with profiler, session.begin(subtransactions=True):
            session.add(_User(name='Bob'))

        assert profiler.count == 1
        assert profiler.insert == 1

    def test_select(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        with profiler:
            session.query(_User).all()

        assert profiler.select == 1

    def test_insert(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        with profiler, session.begin(subtransactions=True):
            session.add(_User(name='Alice'))

        assert profiler.insert == 1

    def test_update(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        profiler.start()

        user = _User(name='Alice')
        with session.begin(subtransactions=True):
            session.add(user)

        with session.begin(subtransactions=True):
            user.name = 'Bob'

        profiler.stop()

        assert profiler.insert == 1
        assert profiler.update == 1

    def test_delete(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        profiler.start()

        user = _User(name='Alice')
        with session.begin(subtransactions=True):
            session.add(user)

        with session.begin(subtransactions=True):
            session.delete(user)

        profiler.stop()

        assert profiler.insert == 1
        assert profiler.delete == 1

    def test_statements(self):
        connection = self.engine.connect()

        profiler = StatementProfiler(self.engine)
        with profiler:
            connection.execute('SELECT 1')

        assert profiler.count == 1
        assert profiler.statements[0] == 'SELECT 1'

    def test_statements_with_params(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        with profiler, session.begin(subtransactions=True):
            session.add(_User(name='Alice'))

        assert profiler.count == 1

        statement, params = profiler.statements_with_parameters[0]
        assert statement.find('INSERT') == 0
        assert len(params) == 1
        assert params[0] == 'Alice'

    def test_sequence(self):
        session = self.session_maker()

        profiler = StatementProfiler(self.engine)
        profiler.start()

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

        profiler.stop()

        # [I]NSERT -> [U]PDATE -> [S]ELECT -> [D]ELETE
        assert profiler.sequence == 'IUSD'


if __name__ == '__main__':
    unittest.main()
