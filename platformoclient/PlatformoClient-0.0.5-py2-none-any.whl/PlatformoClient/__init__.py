#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import calendar
import requests
import time
from threading import Lock

from flask import request
from werkzeug.utils import cached_property
from concurrent.futures import ThreadPoolExecutor

from PlatformoClient.monitor_thread import MonitorThread
from dict_broker import DictBroker
from uwsgi_cache_broker import UwsgiCacheBroker

class PlatformoClient(object):
    def __init__(self, logstash_endpoint, username, \
                 password, interval=10 * 60 * 1000, max_queue_count=10, thread_count=1, broker=None):
        self.username = username
        self.password = password
        self.interval = interval
        self.logstash_endpoint = logstash_endpoint
        self.max_queue_count = max_queue_count
        self.queue_count = 0
        self.lock = Lock()

        if broker:
            self.path_cache = broker
        else:
            try:
                self.path_cache = UwsgiCacheBroker()
            except ImportError:
                self.path_cache = DictBroker()

        self.watching = False
        self.executor = ThreadPoolExecutor(max_workers=thread_count)

    def _interceptor(self, flask_app):
        @flask_app.before_request
        def request_interceptor():
            request.request_time = self._current_milli_time()

        @flask_app.after_request
        def response_interceptor(response):
            self._on_response(response)
            return response

    @cached_property
    def _get_auth_header(self):
        if not self.username:
            return None

        base64_string = base64.encodestring('%s:%s' % (self.username, self.password))[: -1]
        auth_header = 'Basic %s' % base64_string
        return auth_header

    def _send_message(self, message):
        try:
            result = requests.post(self.logstash_endpoint, headers={
                'Content-Type': 'application/json',
                'Authorization': self._get_auth_header
            }, json=message)
        except requests.exceptions.RequestException:
            pass

    def _current_milli_time(self):
        return int(round(time.time() * 1000))

    def _increase_queue_count(self):
        self.lock.acquire()
        self.queue_count += 1
        self.lock.release()

    def _decrease_queue_count(self, future):
        self.lock.acquire()
        self.queue_count -= 1
        if self.queue_count < 0:
            self.queue_count = 0
        self.lock.release()

    def _on_response(self, response):
        self.lock.acquire()
        if self.watching and self.queue_count < self.max_queue_count:
            self.lock.release()
            cache_time = self.path_cache.get(request.path)
            now = self._current_milli_time()
            if not cache_time or \
                            now - int(cache_time) > self.interval:
                self.path_cache.put(request.path, str(now))
                response_duration = now - request.request_time
                message = {
                    'remote_addr': request.remote_addr,
                    'host_addr': request.remote_addr,
                    'path': request.path,
                    'query': request.query_string,
                    'method': request.method,
                    'response_duration': response_duration,
                    'request_utc_time': request.request_time,
                    'status': response.status
                }
                self._increase_queue_count()
                result = self.executor.submit(self._send_message, message)
                result.add_done_callback(self._decrease_queue_count)
        else:
            self.lock.release()

    def watch(self, flask_app):
        self.watching = True
        self._interceptor(flask_app)

    def stop(self):
        self.watching = False
