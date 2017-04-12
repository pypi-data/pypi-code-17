# -*- coding: utf-8 -*-

"""
Takumi-client
=============

Thrift client pool implementation using least connections load balance
strategy capable of invoking an app deployed under multiple servers.

Usage
-----

This module relies on
`takumi-config <https://github.com/elemepi/takumi-config>`_ for settings.

- ``CLIENT_SETTINGS``

  * service: required, service name defined in thrift file
  * thrift_file: required, existing thrift file path
  * pool_size: optional, connection pool size, default 30
  * timeout: optional, connection timeout, default 30s
  * check_time: optional, time interval for checking failed connections,
                default 10s
  * hosts: optional, a list of hosts: [('hostname', port)]
  * extra args: vary for different hosts extensions


Example settings:

.. code:: python

    CLIENT_SETTINGS = {
        'demo': {
            'service': 'PingService',
            'thrift_file': 'ping.thrift',
            'hosts': [
                ('localhost', 1990),
                ('localhost', 8010),
                ('localhost', 1890)
            ]
        }
    }


>>> from takumi_client import clients
>>> pool = clients['demo']
>>> with pool.client_ctx() as c:
...   c.ping()

Extension Protocol
------------------

The pool can be extended using
`takumi-ext <https://github.com/elemepi/takumi-config>`_ to add support for
loading hosts from external resources.

Extension name: ``client-hosts``

.. code:: python

    from takumi_ext import define_ext

    class HostProvider(object):
        def __init__(self, conf, target):
            pass

        def update(self):
            pass

    @define_ext(name='client-hosts')
    def dynamic_hosts_provider(conf):
        '''The entry of the extension.

        :param conf: the config defined in ``CLIENT_SETTINGS``
        :return: The return value should be a class or callable and has methods
                 defined in HostProvider above
        '''
        // ...
        return HostProvider

API
---
"""

from .pool import clients, Pool

__version__ = '0.1.2'
__all__ = ['clients', 'Pool']
