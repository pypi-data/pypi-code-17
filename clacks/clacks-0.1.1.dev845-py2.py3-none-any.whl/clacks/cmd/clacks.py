#!/usr/bin/env python3

"""
Main cherrypy related web application initialization functions
"""

import datetime
import pkgutil
import sys
from os import makedirs

import cherrypy
from cherrypy.lib import profiler
from cherrypy.process import plugins, servers

from ..core import cfg, ROOTPATH
from ..tools import all_subclasses


def getHandlers():

    """Import all handlers from ..handlers package and return them."""

    from .. import handlers
    from ..handlers.URLHandler import URLHandler

    for mdata in pkgutil.iter_modules(handlers.__path__):
        __import__(handlers.__package__+'.'+mdata[1])  # pylint: disable=no-member

    result = {}

    for cls in all_subclasses(URLHandler):
        if cls.mount_url is not None:
            result[cls.mount_url] = cls

    return dict(sorted(result.items(), key=lambda k: k[0]))


def setup():

    """Configure cherrypy to handle all services for a given site."""

    logfile = (ROOTPATH / 'caches/logs/' /
               (lambda d: '%d-%d-%d-error.log' % (d.year, d.month, d.day))(datetime.date.today()))
    makedirs(str(logfile.parent), exist_ok=True)

    config = {
        'environment': 'production' if not cfg.get('__meta__', '__debug', default=False) else None,
        'tools.sessions.on': True,
        'tools.sessions.name': 'clacks',
        'tools.sessions.storage_type': "gtfile",
        'tools.sessions.storage_path': str(ROOTPATH / cfg.get('sessions', 'path', default='data/sessions')),
        'tools.log_tracebacks.on': True,
        'tools.sessions.timeout': 60,
        'tools.sessions.locking': 'explicit',
        'tools.sessions.persistent': False,
        'log.error_file': str(logfile)
        }

    #disabled until it will get reimplemented
    if cfg.get('imports', 'clacks.cptools.i18n_tool', default=None) is not None:
        config.update({
            'tools.I18nTool.on': True,
            'tools.I18nTool.default': cfg.get('locale', 'default-language', default='en_US'),
            'tools.I18nTool.domain': 'python',
        })

    if cfg.get('imports', 'clacks.cptools.sqlalchemy', default=None) is not None:
        config.update({'tools.SATransaction.on': True})

    if cfg.get('imports', 'clacks.cptools.access_grants', default=None) is not None and \
       cfg.get('__meta__', '__debug', default=False):
        config.update({'tools.force_require.on': True})


    cherrypy.config.update(config)

    for path, handler in getHandlers().items():
        cherrypy.tree.mount(
            handler(), path,
            {'/': {'request.dispatch': getattr(cherrypy.dispatch, handler.dispatcher)()}
                  if hasattr(handler, 'dispatcher') else {}})


def start(config=None, daemonize=False, fastcgi=False, port=None):
    """Subscribe all engine plugins and start the engine."""

    engine = cherrypy.engine
    setup()

    for c in config or []:
        cherrypy.config.update(c)

    # Only daemonize if asked to.
    if daemonize:
        # Don't print anything to stdout/sterr.
        cherrypy.config.update({'log.screen': False})
        plugins.Daemonizer(engine).subscribe()

    if hasattr(engine, "signal_handler"):
        engine.signal_handler.subscribe()
    if hasattr(engine, "console_control_handler"):
        engine.console_control_handler.subscribe()

    if fastcgi:
        # Turn off autoreload when using fastcgi.
        cherrypy.config.update({'engine.autoreload.on': False})
        # Turn off the default HTTP server (which is subscribed by default).
        cherrypy.server.unsubscribe()

        def cherryTreeWrapper(environ, start_response):
            environ['SCRIPT_NAME'] = ''
            if False:
               return profiler.make_app(cherrypy.tree, path='/tmp')(environ, start_response)
            else:
                return cherrypy.tree(environ, start_response)

        f = servers.FlupFCGIServer(cherryTreeWrapper, minSpare=1, maxSpare=2)
        s = servers.ServerAdapter(engine, httpserver=f)
        s.subscribe()

    # Always start the engine; this will start all other services
    try:
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.server.socket_port = port
        engine.start()
    except:
        # Assume the error has been logged already via bus.log.
        sys.exit(1)
    else:
        engine.block()


def main():
    from optparse import OptionParser
    from setproctitle import setproctitle

    p = OptionParser()
    p.add_option('-c', '--config', action="append", dest='config',
                 help="specify config file(s)")
    p.add_option('-f', action="store_true", dest='fastcgi',
                 help="start a fastcgi server instead of the default HTTP server")
    p.add_option('-p', '--port', dest='port', default=8080, type=int,
                 help="run the server on port")
    p.add_option('-d', action="store_true", dest='daemonize',
                 help="run the server as a daemon")
    options, args = p.parse_args()

    # shortcut to easily differentiate projects,
    # better solution would be to preserve other options
    setproctitle('clacks --serve '+ROOTPATH.parts[-1])
    start(**vars(options))
