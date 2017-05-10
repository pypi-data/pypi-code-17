"""Operation compiler module."""

from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import CompilerPlugin
from byte.compilers.core.models import InsertOperation, SelectOperation
from byte.statements import InsertStatement, SelectStatement


class OperationCompiler(CompilerPlugin):
    """Operation compiler class."""

    key = 'operation'

    def compile(self, statement):
        """Compile statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement

        :return: Operation
        :rtype byte.compiler.core.models.Operation
        """
        if isinstance(statement, InsertStatement):
            return self.compile_insert(statement)

        if isinstance(statement, SelectStatement):
            return self.compile_select(statement)

        raise NotImplementedError('Unsupported statement: %s' % (statement,))

    def compile_insert(self, statement):
        """Compile insert statement.

        :param statement: Insert statement
        :type statement: byte.statements.InsertStatement

        :return: Insert operation
        :rtype byte.compiler.core.models.InsertOperation
        """
        if statement.properties:
            raise NotImplementedError('"properties" attribute is not supported on insert statements')

        if statement.query:
            raise NotImplementedError('"query" attribute is not supported on insert statements')

        return InsertOperation(
            items=statement.items
        )

    def compile_select(self, statement):
        """Compile select statement.

        :param statement: Select statement
        :type statement: byte.statements.SelectStatement

        :return: Select operation
        :rtype byte.compiler.core.models.SelectOperation
        """
        return SelectOperation(
            where=statement.state.get('where', [])
        )
