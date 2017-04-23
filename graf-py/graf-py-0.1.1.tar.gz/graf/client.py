import socket
import json

from .singleton import Singleton
from datetime import datetime


class Client(Singleton):
    """Graf Client

    Client holds the logic of a Graf client, capable of writing events
    and measuring function execution time.

    Extends:
        Singleton
    """
    @classmethod
    def write(cls, event, data={}):
        """Writes an event to the local Relay

        write is used to quickly write an event to the provided Relay server.
        It assumes the event timestamp as the UTC time based on the local
        machine. If you want to manually specify the timestamp of the event,
        see write_with_time

        Arguments:
            event {string} -- Name of the event being written

        Keyword Arguments:
            data {dict} -- Arbitrary data regarding the event (default: {{}})

        >>> import graf
        ... configure client ...
        >>> graf.Client.write('user_added', { name: 'John' })
        """
        cls.write_with_time(event, datetime.utcnow(), data)

    @classmethod
    def write_with_time(cls, event, time, data={}):
        """Writes an event to the local Relay

        write_with_time writes an event to the provided Relay server. If you
        don't want to specify the event timestamp, use the write function
        instead. When providing the time, make sure it is UTC.

        Arguments:
            event {string} -- Name of the event being written
            time {datetime.datetime} -- datetime instance representing when the
            event occurred

        Keyword Arguments:
            data {dict} -- Arbitrary data regarding the event (default: {{}})

        >>> import graf
        ... configure client ...
        >>> graf.Client.write_with_time('user_added', datetime.utcnow(), { name: 'John' })
        """
        cls.instance().write_packet({
            'e': event,
            't': time.isoformat(),
            'd': data,
        })

    @classmethod
    def configure(cls, server, application, port=2710):
        """Configures the Graf Client singleton

        Configure must be called before writing events. Attempts to write on an
        unconfigured instance are ignored.

        Arguments:
            server {string} -- Hostname or address of the local Relay server.
            application {string} -- Name of the application to which this client
            is bound to.

        Keyword Arguments:
            port {number} -- Port in which your relay server is listening on. (default: {2710})
        """
        cls.instance().set_params(server, application, port)

    @classmethod
    def measure(cls, event_type):
        """Utility method used to measure functions runtime

        Measures how long the decorated function takes to execute, and writes
        every call information to the configured Relay server using the
        following format:
        {
            "duration_ms": (float value)
        }

        Arguments:
            event_type {string} -- Name of the event to be associated with the
            measurement

        >>> @graf.measure('my_function_delay')
        >>> def my_function():
        >>>     return 1 + 1
        """
        def measure_decorator(function):
            def wrapper(*args, **kwargs):
                func_begin = datetime.utcnow()
                function(*args, **kwargs)
                func_end = datetime.utcnow()
                diff = func_end - func_begin
                cls.write(event_type, { 'duration_ms': (diff.total_seconds() / 1000.0) })
            return wrapper
        return measure_decorator

    @classmethod
    def instance(cls):
        """Returns the current Graf client instance

        The client is a Singleton. This method just returns the singleton
        instance.

        Returns:
            graf.Client -- the shared Graf client instance
        """
        return Client()

    def init(self):
        self.server = None
        self.application = None
        self.port = 2710

    def set_params(self, server, application, port=2710):
        """Configures the instance with the provided parameters

        set_params is called by the configure method and sets the provided
        params internally.

        Arguments:
            server {string} -- Hostname or address of the local Relay server
            application {string} -- Name of the application to which this client
            is bound to.

        Keyword Arguments:
            port {number} -- Port in which your Relay server is listening on. (default: {2710})
        """
        self.server = server
        self.application = application
        self.port = port

    def write_packet(self, data):
        if self.server is None or self.application is None or self.port is None:
            return
        data['a'] = self.application
        self._push_packet(data)

    def _push_packet(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(bytes(json.dumps(data)).encode('utf-8'), (self.server, self.port))
        except:
            pass
