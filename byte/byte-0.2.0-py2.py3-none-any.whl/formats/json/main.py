"""JSON format module."""

from __future__ import absolute_import, division, print_function

from byte.formats.core.base import CollectionFormatPlugin, DocumentFormatPlugin, Format
from byte.formats.json.tasks import JsonSelectTask, JsonWriteTask


class BaseJsonFormat(Format):
    """JSON base format."""

    pass


class JsonCollectionFormat(BaseJsonFormat, CollectionFormatPlugin):
    """JSON collection format."""

    key = 'json:collection'

    class Meta(CollectionFormatPlugin.Meta):
        """JSON collection format metadata."""

        content_type = 'application/json'
        extension = 'json'

    def insert(self, executor, operation):
        """Execute insert operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Insert operation
        :type operation: byte.compilers.core.models.InsertOperation
        """
        return JsonWriteTask(executor, [operation]).execute()

    def select(self, executor, operation):
        """Execute select operation.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Select operation
        :type operation: byte.compilers.core.models.SelectOperation
        """
        return JsonSelectTask(executor, operation).execute()


class JsonDocumentFormat(DocumentFormatPlugin):
    """JSON document format."""

    key = 'json:document'

    class Meta(DocumentFormatPlugin.Meta):
        """JSON document format metadata."""

        content_type = 'application/json'
        extension = 'json'
