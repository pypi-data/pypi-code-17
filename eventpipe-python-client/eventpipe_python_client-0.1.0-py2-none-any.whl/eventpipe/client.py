"""
Event pipeline integration. HTTP workers and send
has been nicely copied from Sentry Raven Python client.
"""
from __future__ import absolute_import, print_function
import atexit
import json
import logging
import os
import os.path
from time import sleep, time
import threading
import socket
import ssl
import sys
import urlparse
from urllib import quote as urllib_quote
import urllib2
import requests


string_types = basestring

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # NOQA

NAME = socket.gethostname() if hasattr(socket, 'gethostname') else None
try:
    # Try for certifi first since they likely keep their bundle more up to date
    import certifi
    CA_BUNDLE = certifi.where()
except ImportError:
    CA_BUNDLE = os.path.join(ROOT, 'data', 'cacert.pem')

TIMEOUT = 1

DEFAULT_TIMEOUT = 10

logger = logging.getLogger('')

has_requests = True


def urlopen(url, data=None, timeout=TIMEOUT, ca_certs=None,
            verify_ssl=False, assert_hostname=None):

    class ValidHTTPSConnection(httplib.HTTPConnection):
        default_port = httplib.HTTPS_PORT

        def __init__(self, *args, **kwargs):
            httplib.HTTPConnection.__init__(self, *args, **kwargs)

        def connect(self):
            sock = socket.create_connection(
                address=(self.host, self.port),
                timeout=self.timeout,
            )
            if self._tunnel_host:
                self.sock = sock
                self._tunnel()

            self.sock = ssl.wrap_socket(
                sock, ca_certs=ca_certs, cert_reqs=ssl.CERT_REQUIRED)

            if assert_hostname is not None:
                match_hostname(self.sock.getpeercert(),
                               self.assert_hostname or self.host)

    class ValidHTTPSHandler(urllib2.HTTPSHandler):

        def https_open(self, req):
            return self.do_open(ValidHTTPSConnection, req)

    if verify_ssl:
        handlers = [ValidHTTPSHandler]
    else:
        try:
            handlers = [urllib2.HTTPSHandler(
                context=ssl._create_unverified_context())]
        except AttributeError:
            handlers = []

    opener = urllib2.build_opener(*handlers)

    return opener.open(url, data, timeout)


def check_threads():
    return True


class Transport(object):
    """
    All transport implementations need to subclass this class
    You must implement a send method (or an async_send method if
    sub-classing AsyncTransport) and the compute_scope method.
    Please see the HTTPTransport class for an example of a
    compute_scope implementation.
    """

    async = False
    scheme = []

    def send(self, data, headers):
        """
        You need to override this to do something with the actual
        data. Usually - this is sending to a server
        """
        raise NotImplementedError


class AsyncTransport(Transport):
    """
    All asynchronous transport implementations should subclass this
    class.
    You must implement a async_send method (and the compute_scope
    method as describe on the base Transport class).
    """

    async = True

    def async_send(self, data, headers, success_cb, error_cb):
        """
        Override this method for asynchronous transports. Call
        `success_cb()` if the send succeeds or `error_cb(exception)`
        if the send fails.
        """
        raise NotImplementedError


class HTTPTransport(Transport):
    scheme = ['sync+http', 'sync+https']

    def __init__(self, parsed_url, timeout=TIMEOUT, verify_ssl=False,
                 ca_certs=CA_BUNDLE):
        self._parsed_url = parsed_url
        self._url = parsed_url.geturl().rsplit('+', 1)[-1]

        if isinstance(timeout, string_types):
            timeout = int(timeout)
        if isinstance(verify_ssl, string_types):
            verify_ssl = bool(int(verify_ssl))

        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.ca_certs = ca_certs

    def send(self, data, headers):
        """
        Sends a request to a remote webserver using HTTP POST.
        """
        req = urllib2.Request(self._url, headers=headers)

        try:
            response = urlopen(
                url=req,
                data=data,
                timeout=self.timeout,
                verify_ssl=self.verify_ssl,
                ca_certs=self.ca_certs,
            )
        except urllib2.HTTPError as exc:
            raise
        return response


class AsyncWorker(object):
    _terminator = object()

    def __init__(self, shutdown_timeout=DEFAULT_TIMEOUT):
        check_threads()
        self._queue = Queue(-1)
        self._lock = threading.Lock()
        self._thread = None
        self._thread_for_pid = None
        self.options = {
            'shutdown_timeout': shutdown_timeout,
        }
        self.start()

    def is_alive(self):
        if self._thread_for_pid != os.getpid():
            return False
        return self._thread and self._thread.is_alive()

    def _ensure_thread(self):
        if self.is_alive():
            return
        self.start()

    def main_thread_terminated(self):
        self._lock.acquire()
        try:
            if not self.is_alive():
                # thread not started or already stopped - nothing to do
                return

            # wake the processing thread up
            self._queue.put_nowait(self._terminator)

            timeout = self.options['shutdown_timeout']

            # wait briefly, initially
            initial_timeout = 0.1
            if timeout < initial_timeout:
                initial_timeout = timeout

            if not self._timed_queue_join(initial_timeout):
                # if that didn't work, wait a bit longer
                # NB that size is an approximation, because other threads may
                # add or remove items
                size = self._queue.qsize()

                print("Eventpipe is attempting to send %i pending error messages"
                      % size)
                print("Waiting up to %s seconds" % timeout)

                if os.name == 'nt':
                    print("Press Ctrl-Break to quit")
                else:
                    print("Press Ctrl-C to quit")

                self._timed_queue_join(timeout - initial_timeout)

            self._thread = None

        finally:
            self._lock.release()

    def _timed_queue_join(self, timeout):
        """
        implementation of Queue.join which takes a 'timeout' argument
        returns true on success, false on timeout
        """
        deadline = time() + timeout
        queue = self._queue

        queue.all_tasks_done.acquire()
        try:
            while queue.unfinished_tasks:
                delay = deadline - time()
                if delay <= 0:
                    # timed out
                    return False

                queue.all_tasks_done.wait(timeout=delay)

            return True

        finally:
            queue.all_tasks_done.release()

    def start(self):
        """
        Starts the task thread.
        """
        self._lock.acquire()
        try:
            if not self.is_alive():
                self._thread = threading.Thread(
                    target=self._target, name="eventpipe.AsyncWorker")
                self._thread.setDaemon(True)
                self._thread.start()
                self._thread_for_pid = os.getpid()
        finally:
            self._lock.release()
            atexit.register(self.main_thread_terminated)

    def stop(self, timeout=None):
        """
        Stops the task thread. Synchronous!
        """
        self._lock.acquire()
        try:
            if self._thread:
                self._queue.put_nowait(self._terminator)
                self._thread.join(timeout=timeout)
                self._thread = None
                self._thread_for_pid = None
        finally:
            self._lock.release()

    def queue(self, callback, *args, **kwargs):
        self._ensure_thread()
        self._queue.put_nowait((callback, args, kwargs))

    def _target(self):
        while True:
            record = self._queue.get()
            try:
                if record is self._terminator:
                    break
                callback, args, kwargs = record
                try:
                    callback(*args, **kwargs)
                except Exception:
                    logger.error('Failed processing job', exc_info=True)
            finally:
                self._queue.task_done()

            sleep(0)


class ThreadedHTTPTransport(AsyncTransport, HTTPTransport):

    scheme = ['http', 'https', 'threaded+http', 'threaded+https']

    def get_worker(self):
        if not hasattr(self, '_worker') or not self._worker.is_alive():
            self._worker = AsyncWorker()
        return self._worker

    def send_sync(self, data, headers, success_cb, failure_cb):
        try:
            super(ThreadedHTTPTransport, self).send(data, headers)
        except Exception as e:
            failure_cb(e)
        else:
            success_cb()

    def async_send(self, data, headers, success_cb, failure_cb):
        self.get_worker().queue(
            self.send_sync, data, headers, success_cb, failure_cb)


class RequestsHTTPTransport(HTTPTransport):

    scheme = ['requests+http', 'requests+https']

    def __init__(self, *args, **kwargs):
        self.session = None
        if not has_requests:
            raise ImportError('RequestsHTTPTransport requires requests.')

        super(RequestsHTTPTransport, self).__init__(*args, **kwargs)

    def init_session(self):
        if self.session is None:
            self.session = requests.Session()

    def send(self, data, headers):
        if self.verify_ssl:
            # If SSL verification is enabled use the provided CA bundle to
            # perform the verification.
            self.verify_ssl = self.ca_certs
        self.init_session()
        self.session.post(self._url, data=data, headers=headers,
                          verify=self.verify_ssl, timeout=self.timeout)


class ThreadedRequestsHTTPTransport(AsyncTransport, RequestsHTTPTransport):

    scheme = ['threaded+requests+http', 'threaded+requests+https']

    def get_worker(self):
        if not hasattr(self, '_worker'):
            self._worker = AsyncWorker()
        return self._worker

    def send_sync(self, data, headers, success_cb, failure_cb):
        try:
            super(ThreadedRequestsHTTPTransport, self).send(data, headers)
        except Exception as e:
            failure_cb(e)
        else:
            success_cb()

    def async_send(self, data, headers, success_cb, failure_cb):
        self.get_worker().queue(
            self.send_sync, data, headers, success_cb, failure_cb)


# from config import config

SERVICE = urlparse.urlparse("http://localhost:10000/report")
EVENT_PIPE_ENABLED = True


def okay():
    pass


def fail(*args):
    print('failed', args)

def pipe(service=None):
    service = urlparse.urlparse(service) if service is not None else SERVICE
    transport = ThreadedRequestsHTTPTransport(service)

    def send(data={"ok": 1}, env='dev', success_cb=okay, error_cb=fail, jsonize=False):
        if jsonize:
            data['env'] = env
            data = json.dumps(data)

        transport.async_send(data, {}, success_cb, error_cb)
        return transport

    return send
