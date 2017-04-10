#!/usr/bin/env python3

"""Address composite class."""

# pylint: disable=too-many-arguments, too-many-instance-attributes

from sqlalchemy.ext.mutable import MutableComposite


class Address(MutableComposite):

    """Address composite class.

    \note this is a mixin class that usually shouldn't be instantiated standalone

    example of compatible columns definitions:
        _recipient = Column('recipient', String(512))
        _street = Column('street', String(256))
        _postcode = Column('postcode', String(64))
        _city = Column('post_office', String(256))
        _province = Column('province', String(128))
        _country = Column('country', String(128))
        _lat = Column('lat', Float)
        _lon = Column('lon', Float)
        address = composite(Address,
                            _recipient, _street,
                            _postcode, _city,
                            _province, _country,
                            _lat, _lon)
    """

    def __init__(self, recipient=None, street=None, postcode=None,
                 city=None, province=None, country=None, lat=None, lon=None):
        self.recipient = recipient
        self.street = street
        self.postcode = postcode
        self.city = city
        self.province = province
        self.country = country
        self.lat = lat
        self.lon = lon

    def __setattr__(self, key, value):
        "Intercept set events"

        # set the attribute
        object.__setattr__(self, key, value)

        # alert all parents to the change
        self.changed()

    def __composite_values__(self):
        return (self.recipient, self.street,
                self.postcode, self.city,
                self.province, self.country,
                self.lat, self.lon)

    def __eq__(self, other):
        return isinstance(other, Address) and \
            (other.recipient, other.street,
             other.postcode, other.city,
             other.province, other.country,
             other.lat, other.lon) == \
            (self.recipient, self.street,
             self.postcode, self.city,
             self.province, self.country,
             self.lat, self.lon)

    def update(self, other):
        """Clone all attributes from other instance."""
        self.recipient = other.recipient
        self.street = other.street
        self.postcode = other.postcode
        self.city = other.city
        self.province = other.province
        self.country = other.country
        self.lat = other.lat
        self.lon = other.lon

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__composite_values__())

    def __repr__(self):
        return 'Address(%r, %r, %r, %r, %r, %r, %r, %r)' % self.__composite_values__()

    def export(self):
        """Return JSON compatible dictionary with object state."""
        return {k: v for (k, v) in self.__dict__.items()
                if not k.startswith('_')}
