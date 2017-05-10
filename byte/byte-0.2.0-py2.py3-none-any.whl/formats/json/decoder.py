"""JSON Decoder module."""

from __future__ import absolute_import, division, print_function

import json
import six


class JsonDecoder(object):
    """JSON Decoder."""

    def __init__(self, stream):
        """Create JSON Decoder."""
        self.stream = stream

    @property
    def closed(self):
        """Retrieve boolean representing the decoder "closed" status."""
        return not self.stream or self.stream.closed

    def items(self):
        """Retrieve item iterator."""
        data = json.load(self.stream)

        if type(data) is dict:
            return six.itervalues(data)

        if type(data) is list:
            return data

        raise ValueError('Unsupported data type: %s' % (type(data),))

    def close(self):
        """Close decoder."""
        if not self.stream or self.stream.closed:
            return

        self.stream.close()

    def __enter__(self):
        """Enter decoder context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit decoder context (close decoder)."""
        self.close()
