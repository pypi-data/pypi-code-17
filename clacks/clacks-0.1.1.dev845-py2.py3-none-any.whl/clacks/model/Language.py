#!/usr/bin/env python3

"""Language class."""

from sqlalchemy import Column, Integer, String, Text

from .Base import Base


class Language(Base):

    """Language class."""

    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    native_name = Column(Text, nullable=False)
    iso_code = Column(String(3), nullable=False, unique=True)
    long_code = Column(Text, nullable=False, unique=True)
