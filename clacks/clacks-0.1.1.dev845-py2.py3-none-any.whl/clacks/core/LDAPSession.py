#!/usr/bin/env python3

"""Holds LDAP connection related functions"""

import ldap3

from . import cfg

__all__ = ['get', 'basedn']

basedn = cfg.get('ldap', 'root')


def get():
    """Return LDAP connection to default server."""

    return ldap3.Connection(
        ldap3.Server(cfg.get('ldap', 'host'),
                     port=cfg.get('ldap', 'port', default=389)),
        auto_bind=True,
        user=cfg.get('ldap', 'username'),
        password=cfg.get('ldap', 'password'),
        authentication=ldap3.SIMPLE)
