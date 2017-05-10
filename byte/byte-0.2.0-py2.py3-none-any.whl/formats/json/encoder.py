"""JSON Encoder module."""

from __future__ import absolute_import, division, print_function

from json import JSONEncoder
import six


class JsonEncoder(object):
    """JSON Encoder."""

    def __init__(self, stream, **kwargs):
        """Create JSON Encoder.

        :param stream: Output stream
        :type stream: file or io.IOBase
        """
        self.stream = stream

        self.encoder = JSONEncoder(**kwargs)

    def write_dict(self, items):
        """Write dictionary to stream.

        :param items: Items
        :type items: generator
        """
        for chunk in self.encoder.iterencode(DictionaryEmitter(items)):
            if six.PY3:
                chunk = bytes(chunk, encoding='utf8')

            self.stream.write(chunk)

    def write_list(self, items):
        """Write list to stream.

        :param items: Items
        :type items: generator
        """
        raise NotImplementedError


class DictionaryEmitter(dict):
    """JSON dictionary emitter."""

    def __init__(self, items):
        """Create JSON dictionary emitter.

        :param items: Items
        :type items: generator
        """
        super(DictionaryEmitter, self).__init__()

        self._items = items

    def items(self):
        """Retrieve item iterator."""
        if six.PY2:
            raise Exception('DictionaryEmitter.items() is not supported')

        return self.iteritems()

    def iteritems(self):
        """Retrieve item iterator."""
        for item in self._items:
            yield item

    def __bool__(self):
        """Return boolean representation of instance."""
        return True

    def __nonzero__(self):
        """Return boolean indicating the instance is non-zero."""
        return True

    def __repr__(self):
        """Return python representation of instance."""
        return 'DictionaryEmitter(%r)' % (self._items,)


class ListEmitter(object):
    """JSON list emitter."""

    pass
