from aiohttp.web import Response, WebSocketResponse as AiohttpWebSocketResponse
import aiohttp
from .configuration import override
from .logger import websocket as log
from voluptuous import Optional, Required, All, Range, Any, Schema, ALLOW_EXTRA
import voluptuous


class MsgType:
    AMICONNECT = 'AMICONNECT'
    SUBSCRIBE = 'SUBSCRIBE'
    UNSUBSCRIBE = 'UNSUBSCRIBE'
    CLOSE = 'CLOSE'
    NONE = 'NONE'
    ERROR = 'ERROR'

    ALL = AMICONNECT, SUBSCRIBE, UNSUBSCRIBE, CLOSE, ERROR


class MsgSchema:
    base = Schema({
        Required('type'): Any(*MsgType.ALL)
    }, extra=ALLOW_EXTRA)

    amiconnect = Schema({
        Required('connection'): Schema({
            Required("host"): str,
            Required("port"): str,
            Required("username"): str,
            Required("secret"): str
        }, extra=ALLOW_EXTRA),
        Required('server'): Schema({}, extra=ALLOW_EXTRA)
    }, extra=ALLOW_EXTRA)

    subscribe = Schema({
        Required('uid'): str,
        Required('event'): str,
        Optional('filter'): dict
    }, extra=ALLOW_EXTRA)

    unsubscribe = Schema({
        Required('unuid'): str
    }, extra=ALLOW_EXTRA)

    @classmethod
    def validate(cls, msgpayload, msgtype):
        if msgtype == MsgType.AMICONNECT:
            return cls.amiconnect(msgpayload)
        elif msgtype == MsgType.SUBSCRIBE:
            return cls.subscribe(msgpayload)
        elif msgtype == MsgType.UNSUBSCRIBE:
            return cls.unsubscribe(msgpayload)

        raise voluptuous.Error(f"Unknown msg type {msgtype!s}")


class RequestMsg:
    extra_info = None

    def __init__(self, aiohttp_msg):
        self.original = aiohttp_msg
        try:
            self.payload = self._extract_payload_aiohttp(self.original)
            self.type = self._extract_type_aiohttp(self.original.type, self.payload)
        except Exception as exception:
            self.type = MsgType.ERROR
            self.extra_info = str(exception)
            log.error(self.extra_info)
        else:
            self.payload = MsgSchema.validate(self.payload, self.type)

    def _extract_payload_aiohttp(self, aiohttp_msg):
        return MsgSchema.base(aiohttp_msg.json())

    def _extract_type_aiohttp(self, aiohttp_msg_type, payload):
        if aiohttp_msg_type == aiohttp.WSMsgType.TEXT and 'type' in payload:
            return payload['type']
        elif aiohttp_msg_type == aiohttp.WSMsgType.ERROR:
            return MsgType.ERROR

        return MsgType.NONE


class WebSocketResponse(AiohttpWebSocketResponse):
    import uuid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash = hash(self.uuid.uuid4())

    @property
    def len(self):
        return len(WebSocketResponse.instances)

    @classmethod
    async def instance(cls, request):
        # Factory for async prepare
        self = cls()
        await self.prepare(request)
        return self

    @override
    async def __anext__(self):
        return RequestMsg(await super().__anext__())

    def __hash__(self):
        return self.hash
