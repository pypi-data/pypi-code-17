"""Delete statement module."""

from __future__ import absolute_import, division, print_function

from byte.statements.where import WhereStatement
from byte.statements.write import WriteStatement


class DeleteStatement(WhereStatement, WriteStatement):
    """Delete statement."""

    pass
