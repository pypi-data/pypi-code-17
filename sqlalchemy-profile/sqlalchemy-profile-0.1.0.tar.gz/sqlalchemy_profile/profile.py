# -*- coding: utf-8 -*-

from sqlalchemy.event import listen
from sqlalchemy.event import remove


class StatementProfiler(object):

    def __init__(self, engine):
        self.engine = engine
        self.clear()

    def start(self):
        listen(self.engine, 'after_cursor_execute',
               self._after_cursor_execute_callback)

    def stop(self):
        remove(self.engine, 'after_cursor_execute',
               self._after_cursor_execute_callback)

    def clear(self):
        self._statements = []
        self._parameters = []

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _after_cursor_execute_callback(self, conn, cursor, statement,
                                       parameters, context, executemany):
        self._statements.append(statement)
        self._parameters.append(parameters)

    @property
    def count(self):
        return len(self._statements)

    @property
    def statements(self):
        return self._statements

    @property
    def statements_with_parameters(self):
        return list(zip(self._statements, self._parameters))

    def _query(self, statement_type):
        return [statement
                for statement in self._statements
                if statement.upper().find(statement_type) == 0]

    @property
    def select(self):
        return len(self._query('SELECT'))

    @property
    def insert(self):
        return len(self._query('INSERT'))

    @property
    def update(self):
        return len(self._query('UPDATE'))

    @property
    def delete(self):
        return len(self._query('DELETE'))

    @property
    def sequence(self):
        return ''.join(statement[0].upper()
                       for statement in self.statements)
