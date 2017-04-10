#!/usr/bin/env python3

"""Base LinkNode subclasses creators."""

#pylint: disable=unused-argument

from ..core import cfg
from ..gettext import gettext as _


from ..models import ArticleListNode, ArticleNode, MetaNode, LinkNode
from .. import models

class ArticleFactory(object):

    """Helps to create ArticleNode"""

    @staticmethod
    def getTemplates(parentPage):
        """Return supported template names."""
        if cfg.get('page', 'factory', 'article', 'enabled', default=True):
            return {'article': _('Article')}
        else:
            return {}


    @staticmethod
    def create(parent, method, name, position=None):
        """ Basic article page creation.

        @parent Page instance,
        @method there's only one method, so this parameter
        is not used here,
        @name is used for initial values of linkName, title and urlPart,
        @position needs to be valid numeric position or None, which means append
        """
        node = ArticleNode(linkName=name,
                           title=name,
                           urlPart=name,
                           lang=parent.lang)
        if position is not None:
            parent.childNodes.insert(position, node)
        else:
            parent.childNodes.append(node)

        for ctrldef in sorted(cfg.get('page', 'factory', 'article', 'controls', default={}).values(),
                              key=lambda k: k.get('position', None)):
            ctrl = getattr(models, ctrldef['type'])(**ctrldef.get('args', {}))
            ctrl.dynamic = ctrldef.get('dynamic', False)
            ctrl.placement = ctrldef['placement']
            node.controls.append(ctrl)

        return node


class ArticleListFactory(object):

    """Helps to create ArticleListNode"""

    @staticmethod
    def getTemplates(parentPage):
        """Return supported template names."""
        if cfg.get('page', 'factory', 'articlelist', 'enabled', default=True):
            return {'articlelist': _('Articles list')}
        else:
            return {}


    @staticmethod
    def create(parent, method, name, position=None):
        """ Basic article list type of page creation.

        @parent Page instance,
        @method there's only one method, so this parameter
        is not used here,
        @name is used for initial values of linkName, title and urlPart,
        @position needs to be valid numeric position or None, which means append
        """
        node = ArticleListNode(linkName=name,
                               title=name,
                               urlPart=name,
                               lang=parent.lang)
        if position is not None:
            parent.childNodes.insert(position, node)
        else:
            parent.childNodes.append(node)

        return node


class MetaNodeFactory(object):

    """Helps to create MetaNode"""

    @staticmethod
    def getTemplates(parentPage):
        """Return supported template names."""
        if cfg.get('page', 'factory', 'meta', 'enabled', default=True):
            return {'meta': _('Template page')}
        else:
            return {}


    @staticmethod
    def create(parent, method, name, position=None):
        """ Basic meta page creation.

        @parent Page instance,
        @method there's only one method, so this parameter
        is not used here,
        @name is used for initial value of linkName,
        @position needs to be valid numeric position or None, which means append
        """
        node = MetaNode(linkName=name,
                        lang=parent.lang)
        if position is not None:
            parent.childNodes.insert(position, node)
        else:
            parent.childNodes.append(node)

        return node


class LinkNodeFactory(object):

    """Helps to create LinkNode"""

    @staticmethod
    def getTemplates(parentPage):
        """Return supported template names."""
        if cfg.get('page', 'factory', 'link', 'enabled', default=True):
            return {'link': _('Link')}
        else:
            return {}


    @staticmethod
    def create(parent, method, name, position=None):
        """ Basic link type node creation.

        @parent Page instance,
        @method there's only one method, so this parameter
        is not used here,
        @name is used for initial value of linkName,
        @position needs to be valid numeric position or None, which means append
        """
        node = LinkNode(linkName=name,
                        lang=parent.lang)
        if position is not None:
            parent.childNodes.insert(position, node)
        else:
            parent.childNodes.append(node)

        return node
