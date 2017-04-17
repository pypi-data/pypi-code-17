# -*- coding: utf-8 -*-

"""
takumi_thrift.processor
~~~~~~~~~~~~~~~~~~~~~~~

This module implements an enhanced TProcessor for passing metadata.
"""

import functools
from thriftpy.thrift import TType, TApplicationException, TMessageType
from .wrappers import Response, Metadata


def _unpack(_, n, c, *o):
    return n, c


class Processor(object):
    """Implements Metadata passing

    :param ctx: an object which holds the metadata. The request meta can be
                accessed through the ``meta`` attribute e.g., ``ctx.meta``.
                The attribute ``response_meta`` can be set to pass meta to
                client.
    :param service: thrift service definition
    :param handler: service handler
    """
    def __init__(self, ctx, service, handler):
        self._service = service
        self._handler = handler

        self._ctx = ctx
        self._ctx.meta = {}

    @property
    def _response_meta(self):
        return getattr(self._ctx, 'response_meta', {})

    def _do_process_in(self, iprot, api, seqid):
        if api not in self._service.thrift_services:
            iprot.skip(TType.STRUCT)
            iprot.read_message_end()
            result = TApplicationException(
                TApplicationException.UNKNOWN_METHOD)
            result.oneway = False
            return api, seqid, result, None

        func = getattr(self._handler, api)
        args = getattr(self._service, api + '_args')()
        ret = getattr(self._service, api + '_result')()

        args.read(iprot)
        iprot.read_message_end()
        api_args = [getattr(args, args.thrift_spec[k][1])
                    for k in sorted(args.thrift_spec)]
        call = functools.partial(func, *api_args)
        return api, seqid, ret, call

    def _process_in(self, iprot):
        api, _, seqid = iprot.read_message_begin()
        has_meta = False
        req_meta = {}

        if Metadata.is_meta(api):
            # Receive meta
            meta = Metadata()
            meta.recv(iprot)
            has_meta = True
            req_meta = meta.data
            # Read true message
            api, _, seqid = iprot.read_message_begin()
        return self._do_process_in(iprot, api, seqid), has_meta, req_meta

    def _send(self, oprot, api, data, mtype, seqid, send_meta, meta):
        if send_meta:
            rsp_meta = dict(self._response_meta)
            rsp_meta.update(meta)
            if rsp_meta:
                meta = Metadata(rsp_meta)
                meta.send(oprot, seqid)

        oprot.write_message_begin(api, mtype, seqid)
        data.write(oprot)
        oprot.write_message_end()
        oprot.trans.flush()

    def _process_exception(self, exc, ret):
        spec = list(ret.thrift_spec.items())
        spec.sort(key=lambda x: x[0])

        for name, cls in (_unpack(*s) for _, s in spec):
            if name == 'success':
                continue
            if isinstance(exc, cls):
                setattr(ret, name, exc)
                return True

    def process(self, iprot, oprot):
        """Process rpc request.

        :param iprot: input protocol
        :param oprot: output protocol
        """
        (api, seqid, data, call), has_meta, req_meta = self._process_in(iprot)
        oneway = data.oneway
        meta = {}

        if isinstance(data, TApplicationException):
            mtype = TMessageType.EXCEPTION
        else:
            mtype = TMessageType.REPLY
            try:
                # Set request meta
                self._ctx.meta = req_meta
                # Call handler
                res = call()
                data.success = res
                if isinstance(res, Response):
                    meta = res.meta
                    data.success = res.value
            except TApplicationException as e:
                data = e
                mtype = TMessageType.EXCEPTION
            except Exception as e:
                # Raise if api don't have throws
                if not self._process_exception(e, data):
                    raise
            finally:
                # Reset request meta
                self._ctx.meta = {}

        if not oneway:
            self._send(oprot, api, data, mtype, seqid, has_meta, meta)
