# -*- coding: utf-8 -*-

"""
takumi_thrift
=============

Thriftpy instruments for passing metadata.

:Example:

.. code:: python

    # Server
    class Ctx(object):
        pass
    ctx = Ctx()
    ctx.response_meta = {'server': 'test'}

    class Handler(object):
        def say_hello(name):
            assert ctx.meta == {'hello': 'test', 'client_name': 'test_client'}
            return Response('Hello ' + name, meta={'api': 'say_hello'})

    processor = Processor(ctx, service, Handler())

    # Client
    client = Client(service, proto, meta={'client_name': 'test_client'})
    res = client.call('say_hello', 'world', meta={'hello': 'test'})
    assert res.meta == {'api': 'say_hello', 'server': 'test'}
    assert res.value == 'Hello world'


Request data frame::

    before: message_begin args message_end
    after:  meta_begin meta meta_end message_begin args message_end

Response data frame::

    before: message_begin result message_end
    after:  meta_begin meta meta_end message_begin result message_end

API
---
"""

from .processor import Processor
from .client import Client, ThriftClient
from .wrappers import Response, Metadata
from .exc import TakumiThriftException, TakumiResponseException, \
    UnknownMessageType

__all__ = ['Processor', 'Client', 'Response', 'Metadata', 'ThriftClient',
           'TakumiThriftException', 'TakumiResponseException',
           'UnknownMessageType']
