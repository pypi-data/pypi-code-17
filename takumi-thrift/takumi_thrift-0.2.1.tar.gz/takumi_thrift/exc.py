# -*- coding: utf-8 -*-


class TakumiThriftException(Exception):
    """Represents takumi client related exceptions.
    """


class UnknownMessageType(TakumiThriftException):
    """Raised when received unknown message types.
    """


class TakumiResponseException(TakumiThriftException):
    """Response exception wrapper.
    """
    def __init__(self, exc, meta=None):
        self.meta = meta or {}
        self.exc = exc

    def __getattr__(self, attr):
        return getattr(self.exc, attr)

    def __str__(self):
        return str(self.exc)

    def __repr__(self):
        return repr(self.exc)
