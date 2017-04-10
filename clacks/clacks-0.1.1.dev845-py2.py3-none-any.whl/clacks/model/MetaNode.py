#!/usr/bin/env python3

"""MetaNode class."""

from .SiteNode import SiteNode


class MetaNode(SiteNode):

    """MetaNode class."""

    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'meta'}

    def update(self, items):
        items.update({'visible': False,
                      'placement': ''})
        super().update(items)

    def addNodeGranted(self, user):
        """There's no reason for Meta nodes to chave child nodes"""
        return False
