# -*- coding: utf-8 -*-

"""
This module defines the CacheItem class, which represents key-value pairs that have an
associated time of expiry.
"""

from __future__ import absolute_import

import datetime
import pytz
from . import constants as C

class CacheItem(object):
    """This class represents items, which are key-value pairs that have an associated
    time of expiry.

    :class:`cacheblob.CacheItem`
    """
    def __init__(self, index, value, created=None, expiry=None, duration=None):
        self._index = index
        self._value = None
        self._length = None
        self._created = None
        self._duration = None
        self._expiry = None
        self._updated = None

        if duration is not None and expiry is not None:
            raise ValueError("Cannot simultaneously specify both duration and expiry")

        if created is not None:
            self.created = created
        else:
            self.created = pytz.utc.localize(datetime.datetime.now())

        if expiry is not None:
            self.expiry = expiry
        elif duration is not None:
            self.duration = duration
            self.expiry = self.created + self._duration
        else:
            # This can safely be an else case because of the error thrown earlier
            # Note that if the user wants an item with no expiry, cannot do that here
            self.duration = C.DEFAULT_DURATION
            self.expiry = self.created + self.duration

        self.value = value

    def __str__(self):
        return "{0}:{1}".format(self.index, self.value)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__,
                                  str({'index': self._index,
                                       'value': self._value,
                                       'length': self.length,
                                       'created': self.created,
                                       'duration': self.duration,
                                       'expiry': self.expiry,
                                       'updated': self.updated}))

    @property
    def index(self):
        """Access the index, or key, of a key-value pair.

        :returns: The index, or key, of the key-value pair.
        """
        return self._index

    @index.setter
    def index(self, value):
        """Set the index, or key, of a key-value pair.

        :param value: The value to set.
        """
        self._index = value

    @property
    def value(self):
        """Access the value of a key-value pair.

        :returns: The value of the key-value pair.
        """
        return self._value

    @value.setter
    def value(self, value):
        """Access the value of a key-value pair. This will set the updated field to the
        current time, in UTC.

        :param value: The value to set.
        """
        self._value = value
        self._updated = pytz.utc.localize(datetime.datetime.now())
        if isinstance(value, str):
            self._length = len(value)

    @property
    def duration(self):
        """Access the duration of the key-value pair. This is the length of time that the
        pair was intended to live for.

        :returns: The duration of the key-value pair."""
        return self._duration

    @duration.setter
    def duration(self, value):
        """Set the duration of a key-value pair. If the value is none, then the pair is
        designed to never expire. The duration must be positive.

        :param value: The value to set. Must be a datetime.timedelta value.
        """
        if value is None:
            self._duration = None
            self._expiry = None
            return

        if not isinstance(value, datetime.timedelta):
            raise TypeError("duration must be None or a datetime.timedelta value.")

        if value < datetime.timedelta(0):
            raise ValueError("Duration must be None or positive")

        self._duration = value
        self._expiry = self.created + value

    @property
    def created(self):
        """Access the creation time of the key-value pair, which is stored in UTC.

        :returns: The creation time of the key-value pair."""
        return self._created

    @created.setter
    def created(self, value):
        """Set the creation time of a key-value pair. The time is stored in UTC but does
        not need to be provided as a UTC-localized value.

        :param value: The value to set. Must be a datetime.datetime value.
        """
        if not isinstance(value, datetime.datetime):
            raise TypeError("created must be a datetime.datetime value.")

        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value_utc = pytz.utc.localize(value)
        else:
            value_utc = value

        self._created = value_utc

    @property
    def expiry(self):
        """Access the expiry time of the key-value pair, which is stored in UTC.

        :returns: The expiry time of the key-value pair."""
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """Set the expiry time of a key-value pair. If the value is none, then the pair
        is designed to never expire. The expiry must not be earlier than the creation
        time. The time is stored in UTC but does not need to be provided as a
        UTC-localized value.

        :param value: The value to set. Must be a datetime.datetime value.
        """
        if value is None:
            self._duration = None
            self._expiry = None
            return

        if not isinstance(value, datetime.datetime):
            raise TypeError("expiry must be a datetime.datetime value.")

        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value_utc = pytz.utc.localize(value)
        else:
            value_utc = value

        if value_utc < self.created:
            raise ValueError("Expiry must be None or in the future")

        self._duration = value_utc - self.created
        self._expiry = value_utc

    @property
    def is_expired(self):
        """Determine whether or not the item is expired.

        :returns: Whether the item is currently expired or not.
        """
        return self.expiry < pytz.utc.localize(datetime.datetime.now())

    @property
    def updated(self):
        """Access the last update time of the item.

        :returns: When the item was updated, in UTC.
        """
        return self._updated

    @property
    def length(self):
        """Access the length of the item's value. If the item was a string type then this
        will be the length of the string. Otherwise this will be None, which does not
        indicate that the item has no value.

        :returns: The length of the item's value.
        """
        return self._length
