# -*- coding: utf-8 -*-

"""Start an IPython shell with predefined objects

Usage:
    takumi shell [-t HOST] [(-- <ipython_args>...)]
    takumi shell -h | --help

Options:
    -h, --help       Show this message and exit
    -t, --host HOST  Host the shell client connect to [default: localhost]
"""

import functools
import sys
import importlib

from ._base import parse_args


class _ClientWrapper(object):
    def __init__(self, pool, app):
        self._pool = pool
        self._app = app
        self._thrift = pool.thrift_module
        for func in pool.service.thrift_services:
            api = functools.partial(self.__call, func)
            if func in app.api_map:
                functools.wraps(app.api_map[func].func)(api)
            setattr(self, func, api)

    def __call(self, func, *args, **kwargs):
        with self._pool.client_ctx() as c:
            return getattr(c, func)(*args, **kwargs)


def _create_client_pool(host):
    from takumi_config import config
    if 'CLIENT_SETTINGS' not in config.settings:
        config.settings['CLIENT_SETTINGS'] = {}

    from takumi_client.pool import Pool
    client_name = '{}_shell'.format(config.app_name)

    mod, app = config.app.split(':')
    app = getattr(importlib.import_module(mod), app)
    pool = Pool(client_name, app.thrift_module, app.service_name,
                hosts=[(host, config.port)],
                client_version=config.version or '-')
    c = _ClientWrapper(pool, app)
    return c


def run(args):
    args = parse_args('shell', __doc__, args, {
        '<ipython_args>': list,
        '--host': str,
    })

    import gevent.monkey
    gevent.monkey.patch_all()
    from takumi_config import config

    client = _create_client_pool(args['--host'])
    banner = """Python {}

Interactive shell for service {}.
c         -> Client for invoking service api.
c._thrift -> Loaded thrift module.
config    -> Config entry.
""".format(sys.version.split('\n')[0].strip(), config.app_name)

    ns = {
        'config': config,
        'c': client
    }

    try:
        from IPython import start_ipython
        from traitlets.config.loader import Config
        c = Config(TerminalInteractiveShell={'banner1': banner})
        start_ipython(config=c, argv=args['<ipython_args>'], user_ns=ns)
    except ImportError:
        from code import interact
        interact(banner=banner, local=ns)
    finally:
        client._pool.close()
