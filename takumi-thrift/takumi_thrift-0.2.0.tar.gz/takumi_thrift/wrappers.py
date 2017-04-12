# -*- coding: utf-8 -*-

"""
takumi_thrift.wrappers
~~~~~~~~~~~~~~~~~~~~~~

Defines Response object for wrapping api result.
"""

from thriftpy.thrift import TMessageType, TPayload, TType


class Response(object):
    """Represents api result with arbitrary optinal metadata

    :param value: the real value this respose represents
    :param meta: metadata relates to this response
    """
    def __init__(self, value, meta=None):
        self.value = value
        self.meta = meta or {}

    def __repr__(self):
        return '<Response {!r}>'.format(self.value)

    def __eq__(self, other):
        return self.value == other.value and self.meta == other.meta


class Metadata(TPayload):
    """Metadata passed between client and server

    :param meta: a dict represents metadata
    """
    thrift_spec = {
        1: (TType.MAP, 'data', (TType.STRING, TType.STRING), False)
    }

    META_API_NAME = '__takumi_meta__'

    def __init__(self, meta=None):
        self.data = meta or {}

    @classmethod
    def is_meta(cls, api_name):
        """Test whether the api is meta

        :param api_name: the api to check
        """
        return api_name == cls.META_API_NAME

    def send(self, oprot, seqid):
        oprot.write_message_begin(self.META_API_NAME,
                                  TMessageType.REPLY, seqid)
        self.write(oprot)
        oprot.write_message_end()

    def recv(self, iprot):
        self.read(iprot)
        iprot.read_message_end()
