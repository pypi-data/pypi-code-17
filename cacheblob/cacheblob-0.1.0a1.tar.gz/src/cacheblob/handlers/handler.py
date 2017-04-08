# -*- coding: utf-8 -*-

"""
This module provides base handler functions, and basic functionality. Will
successfully operate as a handler, but if used as one will only store data in-memory.
"""

from __future__ import absolute_import

import cacheblob
from .. import constants as C
from ..item import CacheItem

def is_number(value):
    """Return if value is numeric, based on attempting to coerce to float.

    :param value: The value in question.
    :returns: True if the float(value) does not throw an exception, otherwise False.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

class Handler(object):
    """This module represents a handler for `cacheblob.item` objects. Handlers offer
    simple fetch() and store() capabilities, and other utilities. Items included are
    expected to be unique by index.
    """
    def __init__(self, opts=None):
        self._overwrite = True
        self._index_memoized = {}
        self._memoize = True
        self._memoize_max_length = C.MEMOIZE_MAX_LENGTH
        self._memoize_max_entries = C.MEMOIZE_MAX_ENTRIES
        self._may_purge_if_expired = True

        if opts is not None:
            if 'overwrite' in opts:
                self.overwrite = opts['overwrite']

            if 'memoize' in opts:
                self.memoize = opts['memoize']

            # This is the maximum value length that can be held in a memoized item.
            if 'memoize_max_length' in opts:
                if not self.memoize or ('memoize' in opts and not opts['memoize']):
                    raise ValueError("memoize_max_length ony applicable if memoize is true")
                self.memoize_max_length = opts['memoize_max_length']

            # This is the maximum number of items that will be memoized.
            if 'memoize_max_entries' in opts:
                if not self.memoize or ('memoize' in opts and not opts['memoize']):
                    raise ValueError("memoize_max_entries ony applicable if memoize is true")
                self.memoize_max_entries = opts['memoize_max_entries']

            # This is whether or not the handler can purge expired items from the
            # underlying storage. This is not a promise that it necessarily will.
            if 'may_purge_if_expired' in opts:
                self.may_purge_if_expired = opts['may_purge_if_expired']

    def __iter__(self):
        return self.fetch_all()

    def __contains__(self, index):
        for item in self.fetch_all():
            if item.index == index:
                return True
        return False

    @property
    def overwrite(self):
        """Get the overwrite status.

        :returns: Whether or not the object will overwrite entries with the same index.
        """
        return self._overwrite

    @overwrite.setter
    def overwrite(self, enable_overwrite):
        """Define the overwrite status. This is whether or not an existing item will be
        overwriting if a second item with the same index is stored afterwards.

        :param enable_overwrite: Whether or not items should be overwritten by newer ones.
        """
        self._overwrite = bool(enable_overwrite)

    @property
    def memoize(self):
        """Get the memoization status.

        :returns: Whether or not in-memory memoization is enabled.
        """
        return self._memoize

    @memoize.setter
    def memoize(self, enable_memoize):
        """Enable or disable in-memory memoization. This is designed to make accessing
        quicker.

        :param enable_memoize: Whether or not items should be memoized.
        """
        self._memoize = bool(enable_memoize)

    @property
    def may_purge_if_expired(self):
        """Returns whether or not expired items may be purged from the underlying
        persistent data store. Note that this does not guarantee that they will be
        purged, but instead allows them to be purged.

        :returns: Whether items may be purged if they are expired.
        """
        return self._may_purge_if_expired

    @may_purge_if_expired.setter
    def may_purge_if_expired(self, allow_purge):
        """Enable or disable purging of the underlying data storage upon item expiry.
        This is not a promise that it necessarily will, be if enabled will allow the
        handler to clean purged data as it pleases. Accessing an expired item should not
        be affected by whether this is set or not.

        :param allow_purge: Whether or not purging of expired items is allowed.
        """
        self._may_purge_if_expired = bool(allow_purge)

    @property
    def memoize_max_length(self):
        """Get the max value length allowed for memoized items.

        :returns: The maximum value length allowed for items memoized.
        """
        return self._memoize_max_length

    @memoize_max_length.setter
    def memoize_max_length(self, max_length):
        """Set the maximum value length of items that can be memoized. Note that this is
        not the maximum number of items that can be memoized, but instead the max size of
        them individually.

        :param max_length: The maximum value length allowed.
        """
        if is_number(max_length):
            self._memoize_max_length = max_length
        else:
            raise TypeError("memoize_max_length must be numeric")

    @property
    def memoize_max_entries(self):
        """Get the max number of memoized items at a given time.

        :returns: The maximum number of items that will be memoized.
        """
        return self._memoize_max_entries

    @memoize_max_entries.setter
    def memoize_max_entries(self, max_entries):
        """Set the maximum number of of items that can be memoized.

        :param max_entries: The maximum number of items that can be memoized.
        """
        if is_number(max_entries):
            self._memoize_max_entries = max_entries
        else:
            raise TypeError("memoize_max_entries must be numeric")

    def _get_memoized(self, index):
        """Get the value of a memoized item. This is an internal utility that is not
        designed to be called by users.

        :param index: The index of the item to be retrieved.
        :returns: The item, and whether an item was found or not. If the item is expired
            then it will not be returned, but the second value will be True.
        """
        if self.memoize and index in self._index_memoized:
            item = self._index_memoized[index]
            # Memoized items are easy to purge, so we do so if applicable.
            if self.may_purge_if_expired and item.is_expired:
                self.purge(index)
                return None, True
            return item, True

        return None, False

    def _memoize_if_applicable(self, item):
        """Memoize an item, if enabled. This is an internal utility that is not designed
        to be called by users.

        :param item: The item to be stored.
        :returns: True if an item was stored, otherwise False.
        """
        if self.memoize and (not item.length or item.length <= self.memoize_max_length):
            if item.index not in self._index_memoized or self.overwrite:

                # Remove an arbitrary existing item.
                if (self.memoize_max_entries is not None and
                        len(self._index_memoized) >= self.memoize_max_entries):
                    self._index_memoized.popitem()
                self._index_memoized[item.index] = item
                return True

        return False

    def _delete_memoized(self, index):
        """Delete a memoized item. This is an internal utility that is not designed to be
        called by users. Note that this does not remove an item from the persistent
        storage mechanism.

        :param index: The index of the item to be deleted.
        :returns: True if an item was removed, otherwise False.
        """
        if index in self._index_memoized:
            del self._index_memoized[index]
            return True

        return False

    def _store_item(self, item):
        """Store an item in the handler.

        :param item: The item to be stored.
        :returns: True if the item was successfully stored, False otherwise.
        """
        return self._memoize_if_applicable(item)

    def get_indexes(self):
        """Get all of the indexes stored in the handler.

        :returns: The list of indexes.
        """
        return list(self._index_memoized.keys())

    def purge(self, index):
        """Purge an item from the handler. The persistent value will be removed.

        :param index: The index of the item to be purged.
        :returns: Whether or not an item was removed.
        """
        return self._delete_memoized(index)

    def purge_if_expired(self, index):
        """If an item is expired, purge it.

        :param index: The index of the item to be purged.
        :returns: Whether or not an item was removed.
        """
        (item, found) = self.fetch_with_status(index)

        if (item and item.is_expired) or (found and not item):
            self.purge(index)
            return True

        return False

    def purge_any_expired(self):
        """Purge any items that can be purged, based on their expiry.

        :returns: Count of items purged.
        """
        purged_count = 0

        for index in self.get_indexes():
            if self.purge_if_expired(index):
                purged_count += 1

        return purged_count

    def store(self, *args, **kwargs):
        """Store an entry in the handler. Parameters can be either a `CacheItem`
            or parameters to create one
        
        :param args|item: a `CacheItem` object, or arguments to create one.
        :param kwargs: Keyword arguments to create a `CacheItem` object.
        """

        if len(args) and isinstance(args[0], cacheblob.item.CacheItem):
            return self._store_item(args[0])
        else:
            item = CacheItem(*args, **kwargs)
            return self._store_item(item)

    def fetch(self, index):
        """Fetch an item from the handler.

        :param index: Index of the item to fetch. Indexes are expected to be unique at
            any given time.
        :returns: The item, or None if no unexpired items are found.
        """
        (item, _) = self._get_memoized(index)
        return item

    def fetch_with_status(self, index):
        """Fetch an item from the handler. This differs from fetch() because it will also
        return whether or not an item was found, which differs in the case of expired
        items.

        :param index: Index of the item to fetch. Indexes are expected to be unique at
            any given time.
        :returns: The item, or None if no unexpired items are found, and whether an item
            was found.
        """
        return self._get_memoized(index)

    def fetch_all(self):
        """Fetch all of the items and return an iterator. Note that this function does
        not guarantee that the items will not be modified between this function returning
        and the user accessing the values.

        :returns: An iterator that yields items.
        """
        all_indexes = list(self._index_memoized.keys())
        for index in all_indexes:
            item = self.fetch(index)
            if item:
                yield item

    def fetch_all_with_status(self):
        """Fetch all of the items and return an iterator. Note that this function does
        not guarantee that the items will not be modified between this function returning
        and the user accessing the values. This differs from fetch_all() because it will
        also return whether or not an item was found, which differs in the case of
        expired items.

        :returns: An iterator that yields pairs of items and their status.
        """
        all_indexes = list(self._index_memoized.keys())
        for index in all_indexes:
            yield self.fetch_with_status(index)

    def close(self):
        """Close any associated databases. For this default handler, this does nothing.
        """
        pass
