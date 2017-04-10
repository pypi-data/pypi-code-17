#!/usr/bin/env python3
# pylint: disable=no-member

"""PageNode class."""

import os
import re

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property

from ..core import ROOTPATH
from ..db import db
from ..gettext import gettext as _
from .SiteNode import SiteNode


class PageNode(SiteNode):

    """PageNode class."""

    __tablename__ = 'pages'
    __mapper_args__ = {'polymorphic_identity': 'page'}

    _styles = {}
    _stylesPath = str(ROOTPATH/'http/_styles')

    id = Column('id',
                ForeignKey('links.id', onupdate='CASCADE', ondelete='CASCADE', deferrable=True),
                primary_key=True)
    title = Column(String)
    style = Column(String(32), server_default='', nullable=False)
    _url = Column('url', String(1024))
    _isBase = Column('isbase', Boolean, server_default='false', nullable=False)
    noIndex = Column('noindex', Boolean, server_default='false')
    _urlPart = Column('url_part', String(256))

    @hybrid_property
    def isBase(self):
        """Get isBase value as property"""
        return self._isBase

    @isBase.setter
    def isBase(self, isBase):
        """Set isBase value and refresh all child nodes"""
        self._isBase = isBase
        self.refreshSubtree()

    @hybrid_property
    def url(self):
        """Get url, it is read only."""
        return self._url

    @hybrid_property
    def urlPart(self):
        """get urlPart"""
        return self._urlPart

    @urlPart.setter
    def urlPart(self, urlPart):
        """set urlPart"""
        from gtcms.tools import urlify
        if urlPart:
            self._urlPart = urlify(urlPart)
            if self.isBase:
                self.refreshSubtree()
            else:
                self.rebuildUrl()
        elif self.urlPart is None:
            raise ValueError("urlPart can't be set to None if it already has a value")
        else:
            raise ValueError("empty urlPart not allowed (yet?)")
        db.flush()

    # pylint: disable=no-member
    def rebuildUrl(self):
        """go throug whole subtree and reconstruct all urls"""
        db.flush()
        if self._urlPart:
            url = '/'+self._urlPart+'/'
            node = self.parent

            while node:
                if getattr(node, 'isBase', False) and len(node._urlPart):
                    url = '/'+node._urlPart+url
                node = node.parent

            if self.url:
                oldMatch = re.match('^%s(-([0-9]+))?/$' % re.escape(url[:-1]), self.url)
                if (oldMatch is not None and
                        db.query(PageNode).filter(
                            PageNode.url == self.url,
                            PageNode.id != self.id).count() is None):
                    # old url matches new one and is unique - nothing to do
                    return

            step, baseurl = 0, url[:-1]
            while (db.query(PageNode).filter(PageNode.url == url,
                                             PageNode.id != self.id).count()):
                step += 1
                url = '%s-%d/' % (baseurl, step)

            self._url = url
            db.flush()

    def refreshSubtree(self):
        """Call rebuildUrl on changes"""
        self.rebuildUrl()
        super().refreshSubtree()

    def copyTo(self, node):
        """Clone method specialized to fix urls"""
        newnode = super().copyTo(node)
        newnode.rebuildUrl()
        return newnode

    def export(self):
        """Export object state as JSON compatible dictionary."""
        result = super().export()
        result.update({attr: getattr(self, attr) for attr in
                       ['title', 'style', 'url', 'isBase', 'urlPart', 'noIndex']})
        return result

    def styles(self):
        """List supported styles for this page."""
        if self.type not in self._styles:
            self._styles[self.type] = {}

            for f in (f for f in os.listdir(self._stylesPath)
                      if (os.path.isfile(os.path.join(self._stylesPath, f)) and
                              f.endswith('.css'))):
                with open(os.path.join(self._stylesPath, f), 'r', encoding="utf-8") as fh:
                    lmatch = re.search(r'^/\*\* *Name: *(.*[^ ]) *\*\*/', fh.readline())
                    smatch = re.search(r'^/\*\* *Supports: *.* *article *.*\*\*/', fh.readline())
                    if lmatch and smatch:
                        self._styles[self.type][f[:-4]] = lmatch.groups()[0]
        if not len(self._styles[self.type]):
            self._styles[self.type] = {'': 'default'}

        return self._styles[self.type].copy()

    def update(self, items):
        """Update state from dictionary."""
        super().update(items)
        for key in items.keys():
            if key in ['title', 'style', 'isBase', 'urlPart', 'noIndex']:
                setattr(self, key, items[key])


def __translations():
    """ stub function to keep strings for translation
    so gettext tools can find them """
    return [_('default')]
