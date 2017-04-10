#!/usr/bin/env python3

"""ArticleListNode class."""

from .PageNode import PageNode


class ArticleListNode(PageNode):

    """ArticleListNode class."""

    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'articlelist'}
