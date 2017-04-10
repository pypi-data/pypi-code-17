#!/usr/bin/env python3

"""LinkNode class."""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .SiteNode import SiteNode


class LinkNode(SiteNode):

    """LinkNode class."""

    __tablename__ = 'link_targets'
    __mapper_args__ = {'polymorphic_identity': 'link'}

    _link = Column(ForeignKey('links.id', onupdate='CASCADE', ondelete='SET NULL', deferrable=True),
                   primary_key=True, nullable=False)
    _page = Column(ForeignKey('pages.id', onupdate='CASCADE', ondelete='SET NULL', deferrable=True))
    externalLink = Column('external_link', String(1024))
    localPage = relationship('PageNode', primaryjoin='LinkNode._page==PageNode.id')

    @property
    def url(self):
        """Return target url."""
        if self._page:
            return self.localPage.url

        elif self.externalLink is not None and len(self.externalLink):
            return self.externalLink

        else:
            return None

    def export(self):
        """ node export as dictionary """
        result = super().export()
        result['externalLink'] = self.externalLink
        result['_page'] = self._page
        return result

    def update(self, items):
        """ update contents from dictionary """
        super().update(items)

        if '_page' in items:
            self._page = items['_page'] if isinstance(items['_page'], int) else None

        if 'externalLink' in items:
            self.externalLink = items['externalLink']
