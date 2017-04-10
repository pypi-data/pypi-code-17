#!/usr/bin/env python3

""" UserAddress class """

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import backref, composite, relationship

from .Address import Address
from .Base import Base


class UserAddress(Base):

    """ UserAddress class """

    __tablename__ = 'user_addresses'

    id = Column('id', Integer, primary_key=True)
    # needs to be set not null in the future:
    _user = Column(ForeignKey('clients.id', onupdate='CASCADE', ondelete='CASCADE', deferrable=True))

    recipient = Column('recipient', String(512))
    street = Column('street', String(256))
    postcode = Column('postal_code', String(64))
    city = Column('post_office', String(256))
    province = Column('province', String(128))
    country = Column('country', String(128))
    lat = Column('lat', Float)
    lon = Column('lon', Float)

    label = Column(String, server_default='')
    tags = Column(ARRAY(String))
    created = Column(DateTime, server_default=func.now())

    address = composite(Address,
                        recipient, street,
                        postcode, city,
                        province, country,
                        lat, lon)

    user = relationship('User',
                        backref=backref('addresses',
                                        lazy=True,
                                        cascade='save-update, merge, delete, delete-orphan',
                                        order_by='UserAddress.id'))

    def update(self, **args):
        """Update address record from args dictionary.

        Unknown keys are simply ignored as well as 'created' key,
        so it is easier to send back whole dictionary from jscript
        with some fields unmodified.
        If anything is changed, exact geographical location is set
        to unknown unless it was provided.
        """

        changed = False

        for key, val in args.items():
            if key == 'created':
                continue

            if key == 'id':
                if val != self.id:
                    raise ValueError((key, val))
                else:
                    continue

            if hasattr(self, key):
                if getattr(self, key) != val:
                    setattr(self, key, val)
                    changed = True
            else:
                raise ValueError((key, val))

        if changed and 'lat' not in args:
            if self.lat is not None:
                self.lat = None
            if self.lon is not None:
                self.lon = None

    def export(self):
        """return JSON serialization compatible dictionary"""

        result = {attr: getattr(self, attr) for attr in
                  ['id', 'label', 'tags', 'created']}
        result.update(self.address.export())
        result['created'] = str(result['created'])[:19]
        return result
