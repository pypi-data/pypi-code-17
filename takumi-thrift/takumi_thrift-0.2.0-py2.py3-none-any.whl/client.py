# -*- coding: utf-8 -*-

"""
takumi_thrift.client
~~~~~~~~~~~~~~~~~~~~

This module implements a Thriftpy client which can be used to pass
metadata.
"""

import functools
from copy import deepcopy
from thriftpy.thrift import TMessageType, TApplicationException
from .wrappers import Metadata, Response
from .exc import TakumiThriftException, TakumiResponseException


class Client(object):
    """Thrift Client with metadata supported.

    This class implements a Thrift client which can pass metadata to the
    server.

    :Example:

    >>> c = Client(PingService, iprot, meta={'client_name': 'test',
    ...                                      'client_version': '0.1.0'})
    >>> c.call('say_hello', name='Sarah', meta={'id': 'xxx'})
    >>> # Check server health
    >>> c.check_health()

    :param service: thrift service
    :param iprot: input data protocol
    :param oprot: (optional) output data protocol
    :param meta: (optional) client related metadata passed to server
    """
    HEALTH_CHECK_API_NAME = '__takumi_ping__'

    def __init__(self, service, iprot, oprot=None, meta=None):
        self.service = service
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot

        self._seqid = 0
        self._response_meta = None
        self._support_meta = True
        self.meta = meta or {}

    def _compose_args(self, api, *args, **kwargs):
        args_cls = getattr(self.service, api + '_args')
        arg_names = [i[1] for _, i in sorted(
            args_cls.thrift_spec.items(), key=lambda x: x[0])]
        kw = dict(zip(arg_names, args))
        kw.update({k: v for k, v in kwargs.items() if k in arg_names})
        return kw

    def call(self, api, *args, **kwargs):
        """Call the api.

        If the api is *oneway*, this function will return immediately after
        sending request arguments.

        :param api: api name
        :param meta: (optional) metadata passed to server.
                     Metadata is a dict and keys and values are all str.
        :param \*args: positional arguments passed to the api
        :param \*\*kwargs: keyword arguments passed to the api
        """
        if api not in self.service.thrift_services:
            raise TakumiThriftException(
                'Service {!r} has no such api {!r}'.format(
                    self.service.__name__, api))

        self._send(api, *args, **kwargs)
        ret_cls = getattr(self.service, api + '_result')
        if not ret_cls.oneway:
            try:
                return self._recv(api)
            finally:
                self._response_meta = None

    def _send(self, api, *args, **kwargs):
        kw = self._compose_args(api, *args, **kwargs)
        if self._support_meta:
            data = deepcopy(self.meta)
            data.update(kwargs.pop('meta', {}))
            meta = Metadata(data)
            meta.send(self._iprot, self._seqid)
        self._oprot.write_message_begin(api, TMessageType.CALL, self._seqid)
        args = getattr(self.service, api + '_args')(**kw)
        args.write(self._oprot)
        self._oprot.write_message_end()
        self._oprot.trans.flush()

    def _handle_response(self, res, mtype):
        meta = self._response_meta.data if self._response_meta else {}
        missing = False
        if mtype == TMessageType.EXCEPTION:
            e = res
        else:
            spec = list(res.thrift_spec.items())
            spec.sort(key=lambda x: x[0])
            e = None
            for _, item in spec:
                if item[1] == 'success':
                    # Success
                    if res.success is not None:
                        return Response(value=res.success, meta=meta)
                    missing = True

                e = getattr(res, item[1], None)
                # Exception raised
                if e is not None:
                    break

        if e is None:
            # Void and no exception
            if not missing:
                return Response(None, meta=meta)
            # Missing result
            e = TApplicationException(TApplicationException.MISSING_RESULT)
        raise TakumiResponseException(e, meta)

    def _recv(self, api):
        fname, mtype, _ = self._iprot.read_message_begin()
        if self._support_meta and Metadata.is_meta(fname):
            if mtype == TMessageType.EXCEPTION:
                exc = TApplicationException()
                exc.read(self._iprot)
                self._iprot.read_message_end()
                if exc.type == TApplicationException.UNKNOWN_METHOD:
                    self._support_meta = False
            elif mtype == TMessageType.REPLY:
                meta = Metadata()
                meta.recv(self._iprot)
                self._response_meta = meta
            else:
                raise TakumiThriftException(
                    'Unsupported message type {} for api {!r}'.format(
                        mtype, api))
            # Read real message
            _, mtype, _ = self._iprot.read_message_begin()

        d = TApplicationException() if mtype == TMessageType.EXCEPTION else \
            getattr(self.service, api + '_result')()
        d.read(self._iprot)
        self._iprot.read_message_end()
        return self._handle_response(d, mtype)

    def check_health(self):
        """Check server health.
        """
        try:
            self._oprot.write_message_begin(
                self.HEALTH_CHECK_API_NAME, TMessageType.CALL, self._seqid)
            obj = TApplicationException()
            obj.write(self._oprot)
            self._oprot.write_message_end()
            self._oprot.trans.flush()
            self._iprot.read_message_begin()
            obj.read(self._iprot)
            self._iprot.read_message_end()
            return True
        except Exception:
            return False

    def close(self):
        """Close the transport the client uses.
        """
        self._iprot.trans.close()
        if self._iprot is not self._oprot:
            self._oprot.trans.close()


class ThriftClient(object):
    """Client Wrapper for compatibility.
    """
    def __init__(self, *args, **kwargs):
        self.client = Client(*args, **kwargs)

    def __getattr__(self, attr):
        return functools.partial(self.client.call, attr)

    def __dir__(self):
        return self.client.service.thrift_services

    def close(self):
        self.client.close()
