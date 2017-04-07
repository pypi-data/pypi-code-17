# -*- coding: utf-8 -*-

__author__ = 'zhegz'

import Queue
import threading
import base64
import calendar
from datetime import datetime

import requests

class MonitorThread(threading.Thread):

    def __init__(self, logstash_endpoint, headers, queue, condition):
        super(MonitorThread, self).__init__()
        self.logstash_endpoint = logstash_endpoint
        self.queue = queue
        self.headers = headers
        self.condition = condition

        self.exit_flag = 0


    def run(self):
        self.condition.acquire()
        while not self.exit_flag:

            if not self.queue.empty():
                message = self.queue.get()
                try:
                    requests.post(self.logstash_endpoint, headers=self.headers, json=message)
                except requests.exceptions.RequestException:
                    pass
            else:
                self.condition.wait(timeout=10)

        self.condition.release()


    def stop(self):
        self.exit_flag = 1
