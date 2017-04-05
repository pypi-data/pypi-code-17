#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import calendar
import requests
from threading import Lock
from datetime import datetime

from flask import request
from werkzeug.utils import cached_property
from concurrent.futures import ThreadPoolExecutor

from PlatformoClient.monitor_thread import MonitorThread


class PlatformoClient(object):
    def __init__(self, logstash_endpoint, username, \
                 password, interval=10 * 60 * 1000, max_queue_count=10, thread_count=1):
        self.username = username
        self.password = password
        self.interval = interval
        self.logstash_endpoint = logstash_endpoint
        self.path_cache = dict()
        self.max_queue_count = max_queue_count
        self.queue_count = 0
        self.lock = Lock()

        self.watching = False
        self.executor = ThreadPoolExecutor(max_workers=thread_count)

    def _interceptor(self, flask_app):
        @flask_app.before_request
        def request_interceptor():
            request.request_time = datetime.now()

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

    def _duration_milliseconds(self, start_time, end_time):
        timedelta = end_time - start_time
        return timedelta.microseconds / 10 ** 3 \
               + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 3

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
            cache_time = None
            if request.path in self.path_cache:
                cache_time = self.path_cache[request.path]

            now = datetime.now()
            if not cache_time or \
                            self._duration_milliseconds(cache_time, now) > self.interval:
                self.path_cache[request.path] = now
                response_duration = self._duration_milliseconds(request.request_time, now)
                message = {
                    'remote_addr': request.remote_addr,
                    'host_addr': request.remote_addr,
                    'path': request.path,
                    'query': request.query_string,
                    'method': request.method,
                    'response_duration': response_duration,
                    'request_utc_time': calendar.timegm(request.request_time.utctimetuple()) * 1000,
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
