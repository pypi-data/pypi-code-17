#!/usr/bin/env python3

"""HeadNode class."""

from ..db import db
from .SiteNode import SiteNode


class HeadNode(SiteNode):

    """HeadNode class. There may be only one instance of it.

    Special root node class, shouldn't be crated directly, but only
    during new site creation by calling HeadNode.get() for the first time.
    """

    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'head'}

    @classmethod
    def get(cls):
        """Return the only HeadNode object. Create it first if necessary"""
        node = db.query(HeadNode).get(1)
        if not node:
            node = HeadNode(id=1, linkName='', visible=True, lang='')
            # push sequence forward to prevent uniqueness issues on fresh db
            db.execute("SELECT nextval('links_id_seq')").scalar()
            db.add(node)
            db.flush()
        return node

    def __init__(self, **kwargs):
        if kwargs.get('id', 1) != 1:
            raise ValueError("id argument given but different than 1")
        kwargs['id'] = 1
        super().__init__(**kwargs)
        self._position = 1
        self.placement = 'head'
