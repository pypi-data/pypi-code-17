# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import threading


class GlobalRequestMiddleware(object):
    thread_local = threading.local()

    def process_request(self, request):
        GlobalRequestMiddleware.thread_local.request = request
