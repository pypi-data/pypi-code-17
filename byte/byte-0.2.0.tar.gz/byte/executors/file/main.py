"""File executor module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base import FormatExecutorPlugin
from byte.executors.file.revision import FileRevision

import logging
import os
import six

log = logging.getLogger(__name__)


class FileExecutor(FormatExecutorPlugin):
    """File executor class."""

    key = 'file'

    class Meta(FormatExecutorPlugin.Meta):
        """File executor metadata."""

        scheme = 'file'

    def __init__(self, collection, model):
        """Create file executor.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model
        """
        super(FileExecutor, self).__init__(collection, model)

        # Retrieve path
        self.path = os.path.abspath(self.collection.uri.netloc + self.collection.uri.path)

        if not self.path:
            raise ValueError('Invalid collection path')

        # Retrieve directory
        self.directory = os.path.dirname(self.path)

        # Retrieve file extension
        self.name, self.extension = os.path.splitext(self.path)

        if not self.extension:
            raise ValueError('No file extension defined with collection path')

    def construct_format(self):
        """Construct format parser."""
        return self.plugins.get_collection_format_by_extension(self.extension[1:])()

    def execute(self, statement):
        """Execute statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement
        """
        operation = self.compiler.compile(statement)

        if not operation:
            raise ValueError('Empty statement')

        return self.format.execute(self, operation)

    def read(self):
        """Open file read stream.

        :return: Stream
        :rtype: file or io.IOBase
        """
        if six.PY2:
            return open(self.path)

        return open(self.path, encoding='utf8')

    def revision(self):
        """Create revision."""
        return FileRevision(self)
