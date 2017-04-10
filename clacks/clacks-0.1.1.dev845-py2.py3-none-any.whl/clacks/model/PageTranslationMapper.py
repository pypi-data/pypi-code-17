#!/usr/bin/env python3

"""PageTranslationMapper class."""

from sqlalchemy import (Column, ForeignKey, Integer, String, UniqueConstraint,
                        text)
from sqlalchemy.orm import relationship

from .Base import Base


class PageTranslationMapper(Base):

    """PageTranslationMapper class."""

    __tablename__ = 'component_crossLangMenu'
    __table_args__ = (UniqueConstraint('group', 'lang'),)

    id = Column(Integer, primary_key=True)
    group = Column(Integer,
                   server_default=text("currval('\"component_crossLangMenu_id_seq\"'::regclass)"),
                   nullable=False)
    _lang = Column('lang', String(2),
                   ForeignKey('languages.iso_code', onupdate='CASCADE', ondelete='RESTRICT'),
                   nullable=False)
    _page = Column(ForeignKey('pages.id', onupdate='CASCADE', ondelete='CASCADE'),
                   nullable=False, unique=True)

    lang = relationship('Language')
    page = relationship('PageNode')
