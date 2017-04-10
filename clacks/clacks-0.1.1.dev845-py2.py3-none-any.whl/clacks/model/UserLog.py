#!/usr/bin/env python3

"""UserLog class."""

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import backref, relationship

from .Base import Base


class UserLog(Base):

    """UserLog class."""

    __tablename__ = 'clients_log'

    _user = Column('_client',
                   ForeignKey('clients.id', onupdate='CASCADE', ondelete='CASCADE'),
                   primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)
    ip = Column(INET, nullable=False)

    user = relationship('User',
                        backref=backref('loginDates',
                                        order_by='UserLog.timestamp',
                                        cascade='all, delete-orphan',
                                        passive_deletes=True))
