#!/usr/bin/env python3

""" ArticleNode class """

from sqlalchemy import Column, ForeignKey, Text

from .PageNode import PageNode


class ArticleNode(PageNode):

    """ ArticleNode class """

    __tablename__ = 'articles'
    __mapper_args__ = {'polymorphic_identity': 'article'}

    id = Column('_page', ForeignKey('pages.id', onupdate='CASCADE', ondelete='CASCADE'),
                primary_key=True)
    body = Column(Text)

    def export(self):
        """ export customization used mainly for JSON output """
        result = super().export()
        result['body'] = self.body
        return result

    def update(self, items):
        """ customization to support .body attribute"""
        super().update(items)
        for key in items.keys():
            if key in ['body']:
                setattr(self, key, items[key])
