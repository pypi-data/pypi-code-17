# -*- coding: utf-8 -*-

__author__ = 'zhegz'

import Queue
import threading
import base64
import requests
import calendar
from datetime import datetime
from flask import request
from werkzeug.utils import cached_property


_monitor_thread = None

def create_thread(flask_app, logstash_endpoint, username, password, interval=10 * 60 * 1000):
    global _monitor_thread
    _monitor_thread = MonitorThread(logstash_endpoint, username, password, interval)

    @flask_app.before_request
    def request_interceptor():
        request.request_time = datetime.now()

    @flask_app.after_request
    def response_interceptor(response):
        if _monitor_thread:
            _monitor_thread.on_response()

        return response

    return _monitor_thread


def get_thread():
    return _monitor_thread


class MonitorThread(threading.Thread):

    def __init__(self, logstash_endpoint, username, password, interval=10 * 60 * 1000):
        super(MonitorThread, self).__init__()
        self.logstash_endpoint = logstash_endpoint
        self.username = username
        self.password = password
        self.interval = interval
        self.path_cache = dict()

        self.condition = threading.Condition()
        self.queue = Queue.Queue()

        self.exit_flag = 0


    def run(self):
        self.condition.acquire()
        while not self.exit_flag:

            if not self.queue.empty():
                message = self.queue.get()
                try:
                    requests.post(self.logstash_endpoint, headers={
                        'Content-Type': 'application/json',
                        'Authorization': self._get_auth_header
                    }, json=message)
                except requests.exceptions.RequestException:
                    pass
            else:
                self.condition.wait(timeout=10)

        self.condition.release()


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
        self.condition.notify()
        self.condition.release()


    def _duration_milliseconds(self, start_time, end_time):
        timedelta = end_time - start_time
        return (timedelta.microseconds / 10 ** 3 \
            + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 3)


    def on_response(self):
        if self.exit_flag != 1:
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
                    'request_utc_time': calendar.timegm(request.request_time.utctimetuple()) * 1000
                }
                self._push_message(message)


    def stop(self):
        self.exit_flag = 1
