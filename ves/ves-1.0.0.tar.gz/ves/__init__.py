# -*- coding: utf-8 -*-
import logging
import time
import json

Logger = logging.getLogger(__name__)


class T(object):
    type = 'gevent'  # threading or gevent

    def __init__(self):
        try:
            from gevent.pool import Group
            from gevent.monkey import patch_all
            patch_all()
            self.Thread = Group().spawn
        except Exception as e:
            print 'failed to import gevent'
            # Logger.warning('failed to import gevent' + repr(e))
            self.type = 'threading'
            from threading import Thread
            self.Thread = Thread

    def thread(self, func, *args):
        if self.type == 'gevent':
            self.Thread(func, *args)
        else:
            self.Thread(target=func, args=args).start()


class Server(object):
    def __init__(self, host=None, port=None,
                 func=None, buf_size=None, _type=None):
        self.Thread = T().thread
        import socket
        self.host = host or '127.0.0.1'
        self.port = port or 5000
        self.buf_size = buf_size or 1024*64
        self.func = func
        self.type = _type or dict()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.bind((self.host, self.port))

    def run(self):
        while True:
            try:
                data, client_addr = self.soc.recvfrom(self.buf_size)
                if isinstance(self.type, dict):
                    data = json.loads(data)
                self.Thread(self.send, data, client_addr)
            except:
                print 'Server Failed time sleep 10 s'
                # Logger.error('Server Failed time sleep 10 s', exc_info=True)
                time.sleep(10)

    def send(self, data, client_addr):
        if self.func:
            resp_data = self.func(data)
        else:
            resp_data = data

        if isinstance(self.type, dict) and isinstance(resp_data, dict):
            resp_data = json.dumps(resp_data)

        self.soc.sendto(resp_data, client_addr)


class Client(object):
    def __init__(self, host=None, port=None, buf_size=None, _type=None):
        self.host = host or '127.0.0.1'
        self.port = port or 5000
        self.buf_size = buf_size or 1024*64
        self.type = _type or dict()
        import socket
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(2)

    def send(self, data):
        if isinstance(self.type, dict) and isinstance(data, dict):
            data = json.dumps(data)
        self.soc.sendto(data, (self.host, self.port))
        resp_data, _ = self.soc.recvfrom(self.buf_size)
        if isinstance(self.type, dict):
            resp_data = json.loads(resp_data)

        return resp_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.soc.close()
