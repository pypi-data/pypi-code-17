#!/usr/bin/env python3

"""DbFeature class."""

from sqlalchemy import Column, Date, String, func

from .Base import Base


class DbFeature(Base):

    """DbFeature class."""

    __tablename__ = 'database_features'

    name = Column(String(64), primary_key=True)
    applied = Column(Date, default=func.now())

    def __init__(self, name, applied=False):
        self.name = name
        if applied:
            self.applied = applied
