#!/usr/bin/env python
# -*- coding: utf-8 -*-

from monitor_thread import create_thread


class PlatformoClient(object):
    def __init__(self, logstash_endpoint, username, password, interval=10 * 60 * 1000):
        self.logstash_endpoint = logstash_endpoint
        self.username = username
        self.password = password
        self.interval = interval

    def watch(self, flask_app):
        thread = create_thread(flask_app, self.logstash_endpoint, self.username, self.password, self.interval)
        thread.daemon = True
        thread.start()
