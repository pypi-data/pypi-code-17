#!/usr/bin/env python3

"""Video class."""


from sqlalchemy import Column, Integer, Text

from .Base import Base


class Video(Base):

    """Video class."""

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
