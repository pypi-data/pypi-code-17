#!/usr/bin/env python3

"""Box class."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text

from .Base import Base


class Box(Base):

    """Box class."""

    __tablename__ = 'boxes'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, server_default='')
    content = Column(Text, nullable=False, server_default='')
    style = Column(String(128), nullable=False, server_default='')
    label = Column(String(128), nullable=False, unique=True)
    lang = Column(ForeignKey('languages.iso_code', onupdate='CASCADE', ondelete='CASCADE'),
                  nullable=False)
