# -*- coding: utf-8 -*-

"""
This module implements a MongoDB handler. It stores the items in a MongoDB database.
"""

from __future__ import absolute_import
import six

import pytz

from ..item import CacheItem
from .handler import Handler

class Mongo(Handler):
    """This class implements a MongoDB handler. It stores the items in a MongoDB
    database."""
    def __init__(self, opts=None):
        super(Mongo, self).__init__(opts)

        self._client = None
        self._database_name = 'cacheblob'
        self._table_name = 'cache'
        self._database = None
        self._table = None

        # This may fail, since Mongo isn't required to install the broader library.
        # I don't want to do anything special with the exception.
        global pymongo
        import pymongo

        if opts is not None:
            if 'mongo_init' in opts:
                self.client = pymongo.MongoClient(*opts['mongo_init'])

            if 'database_name' in opts:
                self.database = opts['database_name']

            if 'table_name' in opts:
                self.table_name = opts['table_name']

        if self.client is None:
            self.client = pymongo.MongoClient()

        self.open_database()

    def open_database(self):
        """Open the mongo database and collection that will contain our items.

        :returns: True if the client could create the database and collection, otherwise
            None.
        """
        if self.client is not None:
            self.database = self.client[self.database_name]
            self.table = self.database[self.table_name]
            return True

        return False

    @property
    def client(self):
        """Get the MongoDB client in use.

        :returns: The MongoDB client.
        """
        return self._client

    @client.setter
    def client(self, client):
        """Set the client in use.

        :param client: The client object.
        """
        if not isinstance(client, pymongo.mongo_client.MongoClient):
            raise TypeError("Must provide a pymongo.mongo_client.MongoClient as the client")

        self._client = client

    @property
    def database_name(self):
        """Get the database name in use.

        :returns: The database name.
        """
        return self._database_name

    @database_name.setter
    def database_name(self, name):
        """Set the database name.

        :param name: The name to use.
        """
        if not isinstance(name, (str, six.text_type)):
            raise TypeError("Must provide a string name for the database")

        self._database_name = name

    @property
    def table_name(self):
        """Get the table name in use.

        :returns: The table name.
        """
        return self._table_name

    @table_name.setter
    def table_name(self, name):
        """Set the table name.

        :param name: The name to use.
        """
        if not isinstance(name, (str, six.text_type)):
            raise TypeError("Must provide a string name for the database")

        self._table_name = name

    @property
    def database(self):
        """Get the database in use. This is an internal utility that is not designed to
        be called by users.

        :returns: The database.
        """
        return self._database

    @database.setter
    def database(self, database):
        """Set the database in use. This is an internal utility that is not designed to
        be called by users.

        :param database: The database object.
        """
        if not isinstance(database, pymongo.database.Database):
            raise TypeError("Must provide a pymongo.database.Database for the database")

        self._database = database

    @property
    def table(self):
        """Get the MongoDB table in use.

        :returns: The table.
        """
        return self._table

    @table.setter
    def table(self, table):
        """Set the table. This is an internal utility that is not designed to be called
        by users.

        :param table: The table.
        """
        if not isinstance(table, pymongo.collection.Collection):
            raise TypeError("Must provide a pymongo.collection.Collection for the table")

        self._table = table

    def get_indexes(self):
        """Get all of the indexes stored in the handler.

        :returns: The list of indexes.
        """
        indexes = []

        existing = self.table.find()
        for row in existing:
            indexes.append(row['lookup_index'])

        return indexes

    def _row_to_item(self, row):
        """For a given row from the database, create an return an appropriate item. This
        is an internal utility that is not designed to be called by users.

        :param row: The database row.
        :returns: An item if it could create one, otherwise None.
        """
        if len(row) != 6:
            raise TypeError("Must provide a list of length 6 to _row_to_iteme, or None")

        value = row['value']
        created = pytz.utc.localize(row['created'])
        expiry = pytz.utc.localize(row['expiry'])

        return CacheItem(index=row['lookup_index'],
                         value=value,
                         created=created,
                         expiry=expiry)

    def _store_item(self, item):
        """Store an item in the handler. The value is stored in files, but the other item
        data is stored in the metadata database.

        :param item: The item to be stored.
        :returns: True if the item was successfully stored, False otherwise.
        """
        existing = self.table.find_one({"lookup_index": item.index})

        did_write = False

        item_dict = {"lookup_index": item.index,
                     "value": item.value,
                     "created": item.created,
                     "expiry": item.expiry,
                     "length": item.length}

        # This is one place where we can have concurrency problems
        if existing is not None:

            if not self.overwrite:
                return False

            result = self.table.update_one({"lookup_index": item.index},
                                           {'$set': {'created': item.created,
                                                     'expiry': item.expiry,
                                                     'length': item.length,
                                                     'value': item.value}},
                                           True)

            # If somehow we did not alter the row that we found (row was purged in between?)
            # then create new row
            if not result.modified_count:
                result = self.table.insert(item_dict)
                if result.modified_count:
                    did_write = True

        else:
            result = self.table.insert_one(item_dict)
            if result.acknowledged:
                did_write = True

        self._memoize_if_applicable(item)

        return did_write

    def fetch(self, index):
        """Fetch an item from the handler.

        :param index: Index of the item to fetch. Indexes are expected to be unique at
            any given time.
        :returns: The item, or None if no unexpired items are found.
        """
        (result, status) = self._get_memoized(index)

        if status is not False:
            return result

        existing = self.table.find_one({"lookup_index": index})

        if not existing:
            return None

        result = self._row_to_item(existing)

        if result is not None and not result.is_expired:
            return result

        return None

    def fetch_with_status(self, index):
        """Fetch an item from the handler. This differs from fetch() because it will also
        return whether or not an item was found, which differs in the case of expired
        items.

        :param index: Index of the item to fetch. Indexes are expected to be unique at
            any given time.
        :returns: The item, or None if no unexpired items are found, and whether an item
            was found.
        """
        (result, status) = self._get_memoized(index)

        if status is not False:
            return (result, status)

        existing = self.table.find_one({"lookup_index": index})
        if not existing:
            return None, False

        result = self._row_to_item(existing)

        if result is None:
            return None, False
        elif result.is_expired:
            return None, True
        else:
            return result, True

    def fetch_all(self):
        """Fetch all of the items and return an iterator. Note that this function does
        not guarantee that the items will not be modified between this function returning
        and the user accessing the values.

        :returns: An iterator that yields items.
        """
        result = self.table.find()
        for record in result:
            item = self._row_to_item(record)

            if item is None or item.is_expired:
                pass
            else:
                yield item

    def fetch_all_with_status(self):
        """Fetch all of the items and return an iterator. Note that this function does
        not guarantee that the items will not be modified between this function returning
        and the user accessing the values. This differs from fetch_all() because it will
        also return whether or not an item was found, which differs in the case of
        expired items.

        :returns: An iterator that yields pairs of items and their status.
        """
        result = self.table.find()
        for record in result:
            item = self._row_to_item(record)

            if item is None:
                yield None, False
                break
            elif item.is_expired:
                yield None, True
            else:
                yield item, False

    def purge(self, index):
        """Purge an item from the handler. The persistent value will be removed.

        :param index: The index of the item to be purged.
        :returns: Whether or not an item was removed.
        """
        status = self._delete_memoized(index)

        existing = self.table.find_one({"lookup_index": index})

        # If we're in a state where the entry only exists in the memoized cache,
        # return status of removing that
        if not existing:
            return status

        result = self.table.delete_one({"lookup_index": index})

        if result.deleted_count:
            return True

        return False

    def close(self):
        """Close the database."""
        self.client.close()
