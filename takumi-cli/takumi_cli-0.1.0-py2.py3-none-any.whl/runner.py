# -*- coding: utf-8 -

"""
takumi_cli.runner
~~~~~~~~~~~~~~~~~

This module implements the `serve` command. This command is used for running
Takumi services using gunicorn gevent worker.

Available hooks:

    - after_load    Hook to be called after app imported
"""

import os
import socket
import sys

import gunicorn.workers
from gunicorn.app.base import Application
from gunicorn.config import Setting, validate_pos_int
from gunicorn.util import import_app
from gunicorn.workers.ggevent import GeventWorker

from takumi_config import config


class Worker(GeventWorker):
    def handle(self, listener, client, addr):
        from takumi.service import TakumiService
        from thriftpy.transport import TSocket

        thrift_service = TakumiService()
        ctx = thrift_service.context
        # clear context
        ctx.clear()
        ctx['client_addr'] = addr[0]
        ctx['client_port'] = addr[1]
        ctx['worker'] = self

        client_timeout = self.app.cfg.client_timeout
        if client_timeout is not None:
            client.settimeout(client_timeout)

        handler_getter = self.app.wsgi()
        thrift_service.set_handler(handler_getter())
        sock = TSocket()
        sock.set_handle(client)

        logger = self.log
        try:
            thrift_service.run(sock)
        except socket.timeout:
            logger.warning('Client timeout: %r', addr)
        except socket.error as e:
            import errno
            if e.args[0] == errno.ECONNRESET:
                logger.debug('%r: %s', addr, str(e))
            elif e.args[0] == errno.EPIPE:
                logger.warning('%r: %s', addr, str(e))
            else:
                logger.exception('%r: %s', addr, str(e))
        except Exception as e:
            logger.exception('%r: %s', addr, str(e))
        finally:
            ctx.clear()

# Replace gunicorn default workers
gunicorn.workers.SUPPORTED_WORKERS.clear()
gunicorn.workers.SUPPORTED_WORKERS[
    'gevent_thriftpy'] = 'takumi_cli.runner.Worker'


class ClientTimeout(Setting):
    name = "client_timeout"
    cli = ["--client-timeout"]
    validator = validate_pos_int
    default = None
    desc = """\
        Seconds to timeout a client if client is silent after this duration
    """


class AppRunner(Application):
    def chdir(self):
        # chdir to the configured path before loading,
        # default is the current dir
        os.chdir(self.cfg.chdir)

        # add the path to sys.path
        sys.path.insert(0, self.cfg.chdir)

    def load(self):
        self.chdir()

        def load_app():
            app = import_app(config.app)
            app.hook_registry.on_after_load()
            return app
        return load_app

    def set_cfg(self):
        self.cfg.set('default_proc_name', config.app_name)
        self.cfg.set('worker_class', 'gevent_thriftpy')
        self.cfg.set('worker_connections', config.worker_connections)
        self.cfg.set('loglevel', 'info')
        self.cfg.set('graceful_timeout', 3)
        self.cfg.set('timeout', config.timeout)
        self.cfg.set('bind', '0.0.0.0:{}'.format(config.port))
        self.cfg.set('workers', config.workers)

        if config.env == 'dev' or config.syslog_disabled:
            self.cfg.set('errorlog', '-')
        else:
            self.cfg.set('syslog', True)
            self.cfg.set('syslog_facility', 'local6')
            self.cfg.set('syslog_addr', 'unix:///dev/log#dgram')

    def init(self, parser, opts, args):
        self.set_cfg()
        self.cfg.set('client_timeout', config.client_timeout)
        self.patch_gunicorn()

    def patch_gunicorn(self):
        import gunicorn.sock

        def _socket_str(self):
            return '%s:%d' % self.sock.getsockname()
        gunicorn.sock.TCPSocket.__str__ = _socket_str
