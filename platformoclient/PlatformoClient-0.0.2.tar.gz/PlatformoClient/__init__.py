#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import threading
import base64
import calendar
from datetime import datetime

from flask import request
from werkzeug.utils import cached_property

from PlatformoClient.monitor_thread import MonitorThread


class PlatformoClient(object):
    def __init__(self, flask_app, logstash_endpoint, username, \
        password, interval=10 * 60 * 1000, queue_count=None, thread_count=1):
        self.username = username
        self.password = password
        self.interval = interval
        self.path_cache = dict()

        self.condition = threading.Condition()
        self.queue = Queue.Queue(queue_count)
        self.threads = []
        self.watching = False
        self._interceptor(flask_app)
        self._create_thread(logstash_endpoint, thread_count)


    def _interceptor(self, flask_app):
        @flask_app.before_request
        def request_interceptor():
            request.request_time = datetime.now()

        @flask_app.after_request
        def response_interceptor(response):
            self._on_response(response)
            return response


    def _create_thread(self, logstash_endpoint, thread_count):
        for i in range(thread_count):
            thread = MonitorThread(logstash_endpoint, {
                'Content-Type': 'application/json',
                'Authorization': self._get_auth_header
            }, self.queue, self.condition)
            thread.daemon = True
            self.threads.append(thread)


    @cached_property
    def _get_auth_header(self):
        if not self.username:
            return None

        base64_string = base64.encodestring('%s:%s' % (self.username, self.password))[: -1]
        auth_header = 'Basic %s' % base64_string
        return auth_header


    def _push_message(self, message):
        self.queue.put(message)

        self.condition.acquire()
        self.condition.notifyAll()
        self.condition.release()


    def _duration_milliseconds(self, start_time, end_time):
        timedelta = end_time - start_time
        return timedelta.microseconds / 10 ** 3 \
            + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 3


    def _on_response(self, response):
        if self.watching and not self.queue.full():
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
                self._push_message(message)


    def watch(self):
        self.watching = True
        for thread in self.threads:
            thread.start()
    
    def stop(self):
        self.watching = False
        for thread in self.threads:
            thread.stop()
