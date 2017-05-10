"""JSON format tasks module."""

from __future__ import absolute_import, division, print_function

from byte.core.models import StreamTask, StreamReadTask, StreamSelectTask, StreamWriteTask, Task
from byte.formats.json.decoder import JsonDecoder
from byte.formats.json.encoder import JsonEncoder


class JsonTask(StreamTask):
    """JSON task base."""

    pass


class JsonReadTask(StreamReadTask, JsonTask):
    """JSON read task."""

    def __init__(self, executor, operation):
        """Create JSON read task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operation: Read operation
        :type operation: byte.compilers.core.models.Operation
        """
        super(JsonReadTask, self).__init__(executor, operation)

        self.decoder = None

    @property
    def state(self):
        """Retrieve task state.

        :rtype: int
        """
        state = super(JsonReadTask, self).state

        if self.decoder is None or state == Task.State.created:
            return Task.State.created

        if self.decoder.closed or state == Task.State.closed:
            return Task.State.closed

        return Task.State.started

    def open(self):
        """Open task."""
        super(JsonReadTask, self).open()

        # Create decoder
        self.decoder = JsonDecoder(self.stream)

    def close(self):
        """Close task."""
        if not super(JsonReadTask, self).close():
            return False

        # Close decoder
        if self.decoder:
            self.decoder.close()

        return True


class JsonSelectTask(StreamSelectTask, JsonReadTask):
    """JSON select task."""

    def decode(self):
        """Decode items."""
        return self.decoder.items()


class JsonWriteTask(StreamWriteTask, JsonTask):
    """JSON write task."""

    def __init__(self, executor, operations):
        """Create JSON write task.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param operations: Write operations
        :type operations: list of byte.compilers.core.models.Operation
        """
        super(JsonWriteTask, self).__init__(executor, operations)

        self.decoder = None

    @property
    def state(self):
        """Retrieve task state.

        :rtype: int
        """
        state = super(JsonWriteTask, self).state

        if self.decoder is None or state == Task.State.created:
            return Task.State.created

        if self.decoder.closed or state == Task.State.closed:
            return Task.State.closed

        return Task.State.started

    def decode(self):
        """Decode items."""
        return self.decoder.items()

    def encode(self, revision, items):
        """Encode items.

        :param revision: Executor revision
        :type revision: byte.executors.file.revision.FileRevision

        :param items: Items to encode
        :type items: dict or list
        """
        # Create encoder
        encoder = JsonEncoder(
            revision.stream,
            indent=4
        )

        # Encode items, and write to revision stream
        encoder.write_dict(items)

    def open(self):
        """Open task."""
        super(JsonWriteTask, self).open()

        # Create decoder
        self.decoder = JsonDecoder(self.stream)

    def close(self):
        """Close task."""
        if not super(JsonWriteTask, self).close():
            return False

        # Close decoder
        if self.decoder:
            self.decoder.close()

        return True
