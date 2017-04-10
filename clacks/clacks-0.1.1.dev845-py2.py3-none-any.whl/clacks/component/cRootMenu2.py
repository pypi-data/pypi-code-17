#!/usr/bin/env python3
# pylint: disable=too-many-instance-attributes,too-many-arguments

"""New root menu implementation, lanugage aware."""

import json
import cherrypy

from ..core import cfg
from ..core.templates import templates
from ..db import db
from ..models import SiteNode
from ..tools import structural
from .Component import Component


class cRootMenu2(Component):

    """Root menu components shows all menu entries matching parameters given.

    @arg placement  where menu will be used in page template,
    @arg types list of page types that will be searched and shown in the menu,
    if empty, [@arg placement] will be used instead,
    @arg template if empty, 'component_menu_'+placement will be used,
    @arg depth maximum depth this menu may achieve, set to 0 or None for infinite,
    @arg root - root element from which menu building needs to be started.
    If numeric, page of given id will be used. If list, first of current or parent pages
    which location matches one of list items will be used as base. If empty, first of
    parent pages matching one @arg types will be searched and then first parent page
    which placement does not match any of @arg types list will be selected.
    @arg expand_active (obsolete) additional hint for template how to render contents
    of nested menu
    """

    def __init__(self, placement, types='', template='',
                 depth=128, root=None, expand_active=True):
        """Constructor, callled automatically from config file parser."""
        super().__init__()
        self.root = None
        self._placement = placement
        self.menutypes = types if types else [placement]
        self.depth = depth
        self.template = template if template else ('component_menu_'+placement)
        self.given_root = root
        self._tree = {}
        self.expand_active = expand_active
        self._menu_state = None

    @structural
    def fetch(self, placement):    # pylint: disable=unused-argument,too-many-branches
        """ return formatted menu structure."""

        body = templates[self.template]

        if self.given_root and self.given_root == '*':
            self.root = self.node

        elif self.given_root and not str(self.given_root).isdecimal():

            link = self.node

            while (link.placement not in self.given_root) and (link.type != 'head'):
                link = link.parent

            if link.type != 'head':
                self.root = link
            else:
                self.root = db.query(SiteNode).filter_by(placement='lang',
                                                         lang=self.node.lang).first()

        elif self.given_root:
            self.root = db.query(SiteNode).get(self.given_root)
        else:
            link = self.node
            try:
                if link.placement in self.menutypes:
                    first = link
                else:
                    first = next(p for p in link.parents if p.placement in self.menutypes)
            except StopIteration:
                if db.query(SiteNode).filter(SiteNode.placement.in_(self.menutypes),
                                             SiteNode.parent == link).count():
                    self.root = link
                else:
                    self.root = db.query(SiteNode)\
                                  .filter_by(placement='lang', visible=True, lang=self.node.lang)\
                                  .first()
            else:
                self.root = next(p for p in first.parents if p.placement not in self.menutypes)

        if self.root:
            # depth+1 and getMenuTree counts its element as the first level
            self._tree = self.root.getMenuTree(self.menutypes, self.depth+1)
            return body(menu=self, this=self, lang=self.node.lang)  # menu is obsolete
        return ''

    def getItems(self, root):
        """ used from template to construct submenus """
        if ((cfg.get('components', 'cRootMenu2', self.placement, 'login_required', default=False) and
             not cherrypy.request.user)):
            return []

        if root.id in self._tree:
            return [item for item in self._tree[root.id] if item.viewGranted(cherrypy.request.user)]
        else:
            cherrypy.log('WARNING: Unoptimized submenu request for node:'+str(root.id))
            return [node for node in root.childNodes
                    if node.visible and (node.placement in self.menutypes)]

    @property
    def menu_state(self):
        """ fetch current menu state, either cached or stored in cookie """
        if self._menu_state is None:

            self._menu_state = []
            cookiedata = cherrypy.request.cookie.get('menustate_'+self._placement, '')
            if cookiedata:
                try:
                    self._menu_state = json.loads(cookiedata)
                except ValueError:
                    pass

            if self.expand_active:
                self._menu_state.extend([self.node.id]+list(n.id for n in self.node.parents))

        return self._menu_state

    def isItemExpanded(self, node):
        """ check if node needs to be rendered as expanded one """
        return node.id in self.menu_state

    def isItemInPath(self, node):
        """ used in template to check if given menu item is parent of current page """
        return node == self.node or node in self.node.parents
