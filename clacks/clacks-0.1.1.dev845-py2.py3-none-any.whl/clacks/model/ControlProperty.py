#!/usr/bin/env python3

"""ControlProperty class."""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from .Base import Base


class ControlProperty(Base):

    """ControlProperty class."""

    __tablename__ = 'control_properties'

    _control = Column(ForeignKey('controls.id', onupdate='CASCADE', ondelete='CASCADE'),
                      primary_key=True)
    name = Column(String(64), nullable=False, primary_key=True)
    value = Column(String, nullable=False)
    control = relationship('Control',
                           backref=backref(
                               "_properties",
                               collection_class=attribute_mapped_collection("name"),
                               cascade="all, delete-orphan"
                           ))
