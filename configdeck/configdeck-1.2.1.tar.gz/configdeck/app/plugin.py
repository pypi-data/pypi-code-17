# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
# Copyright © 2009–2013 Canonical Ltd.
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

from configdeck.schema import Schema


__all__ = [
    'Plugin',
    'PluginManager',
]


class Plugin(object):
    schema = Schema
    enabled = False


class PluginManager(object):
    def __init__(self):
        self.available = self.load()

    @property
    def enabled(self):
        return [cls for cls in self.available if cls.enabled]

    def enable(self, plugin):
        plugin.enabled = True

    def disable(self, plugin):
        plugin.enabled = False

    @property
    def schemas(self):
        return [cls.schema for cls in self.enabled]

    def load(self):
        return []

    def register(self, plugin):
        if plugin not in self.available:
            self.available.append(plugin)
