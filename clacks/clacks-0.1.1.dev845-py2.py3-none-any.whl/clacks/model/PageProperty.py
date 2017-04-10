#!/usr/bin/env python3

""" PageProperty class """

from sqlalchemy import Column, ForeignKey, String

from .Base import Base


class PageProperty(Base):

    """ PageProperty class """

    __tablename__ = 'page_properties'

    _page = Column(ForeignKey('pages.id', ondelete='CASCADE', onupdate='CASCADE'),
                   primary_key=True)
    name = Column(String(255), primary_key=True)
    value = Column(String)
