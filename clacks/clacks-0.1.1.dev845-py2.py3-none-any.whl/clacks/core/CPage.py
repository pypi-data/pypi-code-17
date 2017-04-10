#!/usr/bin/env python3

"""CPage, currently mostly copy-paste reimplementation of PHP code to ease transition."""

from .. import components as Components
from ..core import cfg, env
from ..db import db
from ..core.templates import templates
from ..models import MetaNode
from .BasePage import BasePage


class CPage(BasePage):

    """Session authentication state handler."""

    def __init__(self, node):

        super().__init__()
        self.panels = {}
        self.node = node
        self.addDependencies(cfg.get('page', 'dependencies', 'common', default={}))
        self.addDependencies(cfg.get('page', 'dependencies', self.node.type, default={}))

    def _getMeta(self, node):
        """ Fetch first meta page found.
        \todo: needs optimization (probably involving db model change)
        """
        if not node.parent:
            return None

        meta = db.query(MetaNode).filter_by(parent=node.parent).first()

        return meta if meta else self._getMeta(node.parent)

    def deps(self):
        """ obsolete: temporarily needed by header_dependencies.pt"""
        return self.getDependencies()

    def placeElement(self, elem, location, priority=50):
        """add structural element in a given location."""
        if location not in self.panels:
            self.panels[location] = []
        self.panels[location].append((elem, priority,))
        self.panels[location].sort(key=lambda k: k[1])

    def getPanels(self, location):
        """ return all elements added in a given location in order of preference """
        return [p[0] for p in self.panels[location]] if location in self.panels else []

    def fetch(self):
        """ generate page contents."""
        template = None
        page_type = self.node.type
        template = templates.first('page_'+self.node.type+'_'+self.node.style,
                                   'page_default_'+self.node.style,
                                   'page_'+self.node.type,
                                   'page_default')

        params = {}
        params.update({'handler': self,
                       'node': self.node,  # obsolete
                       'this': self.node,
                       'ctx': self,  # obsolete, but needed by header_dependencies.pt
                       'cfg': cfg,
                       'Env': env})

        params['pagetype'] = page_type

        if self.node.style and (self.node.style != 'default'):
            self.addDependency('css', '/_styles/'+self.node.style+'.css',
                               {'priority': 90})

        components = Components.fetchByType(page_type)

        for component in components:
            component.startup(self.node)
            self.placeElement(component,
                              component.placement)

        controls = []
        metapage = self._getMeta(self.node)
        if metapage:
            controls.extend(metapage.controls)
        controls.extend(self.node.controls)

        for control in controls:
            control.startup(self.node)
            for placement in control.placements:
                self.placeElement(control, placement)

        return template(**params)
