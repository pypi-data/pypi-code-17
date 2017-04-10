#!/usr/bin/env python3

"""Basic page template wrapper."""

from collections import OrderedDict


class BasePage(object):

    """Basic page template wrapper."""

    def __init__(self):
        self._deps = {}
        self._sortedDeps = None

    def addDependencies(self, items):
        """Add page dependencies."""
        for dtype, elem in items.items():
            for dname, dparam in elem.items():
                self.addDependency(dtype, dname, dparam)

    def addDependency(self, dtype, name, params=None):

        """Add single dependency."""

        if params is None:
            params = {}

        self._sortedDeps = None
        params['name'] = name
        params['src'] = params.get('src', name)
        params['priority'] = params.get('priority', '50')

        if dtype not in self._deps:
            self._deps[dtype] = OrderedDict()

        if name not in self._deps[dtype]:
            self._deps[dtype][name] = params
        else:
            if self._deps[dtype][name]['priority'] > params['priority']:
                self._deps[dtype][name]['priority'] = params['priority']

            if self._deps[dtype][name]['src'] != params['src']:
                raise Exception('BasePage::addDependency inconsistency found',
                                (params['src'], self._deps[type][name]))

    def getDependencies(self):
        """Return sorted list of dependencies"""
        if self._sortedDeps is None:
            self._sortedDeps = {}
            for dtype, elem in self._deps.items():
                self._sortedDeps[dtype] = sorted(elem.values(),
                                                 key=lambda p: int(p.get('priority', 0)))
        return self._sortedDeps

    def hasDependency(self, dtype, name):
        """Check if dependency is added already."""
        return any(d['src'] == name for d in self.getDependencies().get(dtype, []))
