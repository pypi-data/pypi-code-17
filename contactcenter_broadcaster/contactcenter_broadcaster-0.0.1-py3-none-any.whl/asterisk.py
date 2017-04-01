from asyncio import sleep, ensure_future, shield, get_event_loop
from panoramisk import Manager as PanoramiskAMIManager
from collections import defaultdict
from .configuration import config, override
from .tool import PubSubSupport
from .exception import AMIStubError
from .websocket import MsgType
from .logger import asterisk as log


class WSMsgDispatcher:
    _connections = []
    # ami manager cace settings
    _usecache = config['application']['usecache']

    def __init__(self, socket, ip=None):
        self._socket = socket
        self._ip = ip
        self._manager = AMIManager.stub()
        self.__class__._connections += socket,

    async def dispatch(self, msg):
        try:
            if msg.type == MsgType.AMICONNECT:
                self._manager = await self._resolve_ami(msg.payload["connection"])
                self._socket.send_json(dict(type="amiconnect"))
            elif msg.type == MsgType.SUBSCRIBE:
                self._manager.subscribe(msg.payload, self._socket)
                log.info("{ip} subscribe for {event} on {uid}".format(**msg.payload, ip=self._ip))
            elif msg.type == MsgType.UNSUBSCRIBE:
                self._manager.unsubscribe(uid=msg.payload['unuid'])
                log.info("{ip} unsubscribe on: {unuid}".format(**msg.payload, ip=self._ip))
            else:
                log.info(f"{self._ip} incorrect message type: {msg.type}")
                self._socket.send_json(dict(type="invalid", code=404))
        except AMIStubError as error:
            self._socket.send_json(dict(type="error", code=401))

    @property
    def len(self):
        return len(self._connections)

    def exit(self):
        try:
            self._manager.unsubscribe(socket=self._socket)
        except AMIStubError as error:
            log.info(error)
        finally:
            self._connections.remove(self._socket)

    def _resolve_ami(self, params):
        """ :rtype Future[AMIMAnager] """

        return shield(AMIManagerCache.getinstance(params) if self._usecache
                      else ensure_future(AMIManager.instance(params)))


class AMIManagerCache:
    _store = defaultdict(None)

    @classmethod
    def getinstance(cls, key: dict):
        """
        :param: key - configuration for AMI connection
        :rtype: Future[AMIManager]
        """

        hash_of_key = hash(str(key))

        if hash_of_key not in cls._store:
            cls._store[hash_of_key] = cls._new_ami_connection(key, hash_of_key)

        return cls._store[hash_of_key]

    @classmethod
    def _new_ami_connection(cls, key, hashkey):
        task = ensure_future(AMIManager.instance(key))

        log.info(f"new AMIManager task with hash {hashkey} push to cache")

        task.add_done_callback(lambda task: task.result().on(
            AMIManagerCloseEvent,
            lambda event: cls._store.pop(hashkey, None)
        ) if not task.cancelled() and task.exception() is None else None)

        return task

    def __getitem__(self, key):
        return self.getinstance(key)

    def __delitem__(self, key):
        del self._store[key]


class AMIManager(PanoramiskAMIManager, PubSubSupport):
    _autofilter = config['asterisk']['ami']['filter']['command']
    _conn_timeout = config['asterisk']['ami']['timeout']

    def __init__(self, params):
        PanoramiskAMIManager.__init__(
            self, loop=get_event_loop(), host=params['host'],
            port=params['port'], username=params['username'],
            secret=params['secret']
        )
        # override for no dublicate items
        # for more info see PanoramiskAMIManager.dispatch()
        self.patterns = self.__distinctlist()
        self._len = 0
        self.__isconnect = False

    def subscribe(self, payload, socket):
        handler = EventHandler(payload, socket)
        handler.on(
            AMIBrockenHandler, lambda event: self.unsubscribe(uid=event.uid))
        self._len += 1
        return self.register_event(payload['event'], handler)

    def unsubscribe(self, *, socket=None, uid=None):

        if not socket and not uid:
            return

        try:
            for callbacks in self.callbacks.values():
                for callback in callbacks[:]:
                    if isinstance(callback, EventHandler):
                        if socket and callback.socket is socket:
                            callbacks.remove(callback.uid)
                            self._len -= 1
                        elif uid and callback.uid == uid:
                            callbacks.remove(callback.uid)
                            self._len -= 1
                            return
        finally:
            if self._len == 0:
                try:
                    self.close()
                except Exception as exception:
                    log.error(exception)
                else:
                    log.info(f"close AMIManager connection")

    @override
    def close(self, *args):
        self.fire(AMIManagerCloseEvent())
        return PanoramiskAMIManager.close(self, *args)

    async def while_not_opened(self):
        self.connect()

        while not self.__isconnect:
            await sleep(1)

        return self

    @override
    def connect(self):

        def on_done_callback(task):
            self.__isconnect = (task.exception() is None and
                                not task.cancelled())

            if not self.__isconnect:
                log.warning("was fail try for connect to AMI")

        task = PanoramiskAMIManager.connect(self)
        task.add_done_callback(on_done_callback)

        return task

    @classmethod
    async def instance(cls, params, *, autostart=True):
        self = cls(params)

        if autostart:
            await self.while_not_opened()

        if autostart and config['asterisk']['ami']['filter']['use']:
            await self._set_event_filter()

        log.info(f"success instance for AMI with params: {params}")

        return self

    @property
    def len(self):
        return self._len

    # helpers
    async def _set_event_filter(self):
        result = await self.send_action(dict(
            Action='Filter',
            ActionID='0001',
            Filter=self._autofilter,
            Operation='Add'
        ))

        if result['Response'] == 'Success':
            log.info(f"success set filter to AMI: {self._autofilter}")
        else:
            log.error(f"error set filter: {result}")

        return result

    class stub:
        """ Always raise exception when call any method """

        def __init__(self, exception=None):
            self.msg = str(exception) if exception else None

        def __getattr__(self, attr):
            raise AMIStubError((
                f"Try to get: {attr} from stub instance AMIManager"
            ) if not self.msg else self.msg)

    class __distinctlist(list):
        """
        For fix ugly feature with `panoramisk.Manager.patterns`.
        For more information see:
        https://github.com/gawel/panoramisk/blob/master/panoramisk/manager.py,
        line 208 register_event, version 1.0 or 1.1
        """

        def append(self, *args, **kwargs):
            if args[0] not in self:
                super().append(*args, **kwargs)


class EventHandler(PubSubSupport):
    def __init__(self, payload, socket):
        self._payload = payload
        self._socket = socket

    def _handle(self, event):
        if self._issuitable(event):
            try:
                self.socket.send_json(dict(
                    type='event', uid=self.uid, payload=dict(**event)))
                log.info(f"fire event {event} for {self.uid}")

            # todo refact this
            except (RuntimeError, ValueError, TypeError) as exception:
                log.error(f"error while send to {self.uid} case: {exception}")
                self.fire(AMIBrockenHandler(self.uid))

    def _issuitable(self, event):
        # :event is Panoramisk dict-like structure

        for key, value in self.filter.items():
            if key not in event or value not in event[key]:
                return False

        return True

    @property
    def filter(self):
        """ filtration by payload filter """

        return {
            key: value for key, value in self.payload['filter'].items()
            if isinstance(value, str) and len(value)
        } if 'filter' in self.payload else {}

    @property
    def payload(self):
        return self._payload

    @property
    def socket(self):
        return self._socket

    @property
    def uid(self):
        return self.payload['uid']

    @property
    def pattern(self):
        return self.payload['event']

    def __call__(self, manager, event):
        return self._handle(event)

    def __eq__(self, other):
        # for correct remove self by uid,
        # example - handlers.remove(uid)
        return (self.uid == other.uid if isinstance(other, type(self))
                else self.uid == other)

    def __repr__(self):
        return "<{0} uid={1}, socket.hash={2}>".format(
            self.__class__.__name__, self.uid, self.socket.hash)


class AMIManagerCloseEvent(PubSubSupport.Event):
    def __init__(self):
        super().__init__('AMIManagerCloseEvent')


class AMIBrockenHandler(PubSubSupport.Event):
    def __init__(self, uid):
        super().__init__(AMIBrockenHandler.__class__)
        self._uid = uid

    @property
    def uid(self):
        return self._uid
