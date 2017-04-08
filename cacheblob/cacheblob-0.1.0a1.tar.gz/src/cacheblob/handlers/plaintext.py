# -*- coding: utf-8 -*-

"""
This module implements a plaintext handler. It stores item values in files on disk and
uses a SQLite database to store the metadata. This is most convenient if you are using
items as files in another way, or otherwise prefer being able to interact with each item
as a file.
"""

from __future__ import absolute_import

import os
import uuid
import pytz

from .. import db_wrapper
from ..item import CacheItem
from .. import constants as C
from .handler import Handler

class Plaintext(Handler):
    """This class implements a plaintext handler which stores items as files on disk,
    with a SQLite database used for the indexing.
    """
    def __init__(self, opts=None):
        super(Plaintext, self).__init__(opts)

        self._index_file = C.DEFAULT_DB_FILE
        self._directory = None
        self._index_absolute = None
        self._database = None

        self._create_index_table = """CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY,
            lookup_index TEXT,
            filename TEXT,
            created TIMESTAMP,
            expiry TIMESTAMP,
            length INTEGER)"""

        if opts:
            if 'directory' in opts:
                self.directory = opts['directory']
            if 'index_file' in opts:
                self.index_file = opts['index_file']

        if self.directory is None:
            self.directory = os.path.join(os.getcwd(), C.DEFAULT_DIRECTORY)

        self.open_database()

    def open_database(self):
        """Open the SQLite database that will be used to store the metadata."""
        self.database = db_wrapper.DBWrapper(self._index_absolute, pytypes=True)
        self.database.init_table('lookup', self._create_index_table)
        self.database.set_update_sql('lookup',
                                     'INSERT OR REPLACE INTO {} VALUES(NULL, ?, ?, ?, ?, ?)')

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
        self._database = database

    @property
    def directory(self):
        """Get the directory in which the item files and SQLite index database are
        stored.

        :returns: The directory used.
        """
        return self._directory

    @directory.setter
    def directory(self, directory):
        """Set the directory to be used for item files and the SQLite index database.

        :param directory: The directory to be used.
        """
        self._directory = directory

        if directory is None:
            return

        if not os.access(directory, os.W_OK):
            os.mkdir(directory)

        self.define_index(directory, self.index_file)

    @property
    def index_file(self):
        """Get the filename of the SQLite database for storing item metadata.

        :returns: The name of the index file.
        """
        return self._index_file

    @index_file.setter
    def index_file(self, filename):
        """Set the filename of the SQLite database for storing item metadata.

        :param filename: The filename to assign, relative to self.directory.
        """
        self._index_file = filename

        self.define_index(self.directory, filename)

    def define_index(self, directory=None, index_file=None):
        """Define the full index file path, based on the directory and index_file. The
        directory and index_file need not be provided here, if previously defined.

        :param directory: The directory to use.
        :param index_file: The SQLite file to use for item metadata.
        """

        if directory and (not self.directory or directory != self.directory):
            self.directory = directory
        if index_file and (not self.index_file or index_file != self.index_file):
            self.index_file = index_file
        self._index_absolute = os.path.join(self.directory, self.index_file)
        self.close()
        self.open_database()

    def get_indexes(self):
        """Get all of the indexes stored in the handler.

        :returns: The list of indexes.
        """
        select_sql = "SELECT lookup_index FROM lookup"

        result = self.database.get_cursor().execute(select_sql)

        if result:
            return [item[0] for item in result.fetchall()]

        return []

    def _open_helper(self, filename, mode):
        """Open a file with the specified mode. This is split out such that we can handle
        plaintext and gzip files without much source duplication. This is an internal
        utility that is not designed to be called by users.

        :param filename: The filename to be opened.
        :param mode: The file mode to open it under, e.g. 'r' or 'w'.
        """
        return open(filename, mode)

    def _row_to_item(self, row):
        """For a given row from the metadata database, create an return an appropriate
        item. This is an internal utility that is not designed to be called by users.

        :param row: The database row.
        :returns: An item if it could create one, otherwise None.
        """
        if row is None:
            return None

        if not isinstance(row, (list, tuple)) or len(row) != 6:
            raise TypeError("Must provide a list/tuple of length 6 to _row_to_item, or None")

        filename = row[2]
        created = pytz.utc.localize(row[3])
        expiry = pytz.utc.localize(row[4])

        path = os.path.join(self.directory, filename)
        if os.path.exists(path):
            with self._open_helper(path, 'r') as in_fh:
                value = in_fh.read()
                in_fh.close()
            found_item = CacheItem(index=row[1],
                                   value=value,
                                   created=created,
                                   expiry=expiry)
            return found_item

        return None

    def _store_item(self, item):
        """Store an item in the handler. The value is stored in files, but the other item
        data is stored in the metadata database.

        :param item: The item to be stored.
        :returns: True if the item was successfully stored, False otherwise.
        """
        select_sql = "SELECT id, filename FROM lookup WHERE lookup_index=? LIMIT 1"

        result = self.database.get_cursor().execute(select_sql, [item.index])
        existing = result.fetchone()

        did_write = False

        # This is one place where we can have concurrency problems
        if existing is not None:
            if not self.overwrite:
                return False

            index_id = existing[0]
            filename = existing[1]

            with self._open_helper(os.path.join(self.directory, filename), 'wb') as out_fh:
                # As long as item.value can have a string representation, it can be stored
                out_fh.write(str(item.value).encode('utf-8'))
                out_fh.close()

                update_sql = "UPDATE lookup SET created=?, expiry=?, length=? WHERE id=?"
                update_list = [item.created, item.expiry, item.length, index_id]
                result = self.database.get_cursor().execute(update_sql, update_list)
                self.database.get_con().commit()

                # If somehow we did not alter the row that we found (row was purged in between?)
                # then create new row
                if result.rowcount == 0:
                    update_list = [item.index, filename, item.created, item.expiry, item.length]
                    self.database.update_db('lookup', update_list)
                    if self.database.get_cursor().rowcount > 0:
                        did_write = True
                else:
                    did_write = True
        else:
            # Generate a new arbitrary filename to be used for the value storage.
            new_filename = str(uuid.uuid4()) + ".data"
            full_filename = os.path.join(self.directory, new_filename)

            if self.overwrite or not os.path.isfile(full_filename):
                with self._open_helper(full_filename, 'wb') as out_fh:
                    out_fh.write(str(item.value).encode('utf-8'))
                    out_fh.close()

            update_list = [item.index, new_filename, item.created, item.expiry, item.length]

            self.database.update_db('lookup', update_list)

            select_sql = "SELECT id FROM lookup WHERE lookup_index=? LIMIT 1"

            result = self.database.get_cursor().execute(select_sql, [item.index])
            if result.fetchone() is not None:
                did_write = True

        self._memoize_if_applicable(item)

        return did_write

    def fetch(self, index):
        """Fetch an item from the handler.

        :param index: Index of the item to fetch. Indexes are expected to be unique at
            any given time.
        :returns: The item, or None if no unexpired items are found.
        """
        (item, status) = self._get_memoized(index)

        if status is not False:
            return item

        select_sql = "SELECT * FROM lookup WHERE lookup_index=? LIMIT 1"

        result = self.database.get_cursor().execute(select_sql, [index])

        data = result.fetchone()

        item = self._row_to_item(data)
        if item is not None and not item.is_expired:
            return item

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
        (item, status) = self._get_memoized(index)

        if status is not False:
            return (item, status)

        select_sql = "SELECT * FROM lookup WHERE lookup_index=? LIMIT 1"

        result = self.database.get_cursor().execute(select_sql, [index])

        data = result.fetchone()

        item = self._row_to_item(data)

        if item is None:
            return None, None
        elif item.is_expired:
            return None, True
        else:
            return item, True

    def fetch_all(self):
        """Fetch all of the items and return an iterator. Note that this function does
        not guarantee that the items will not be modified between this function returning
        and the user accessing the values.

        :returns: An iterator that yields items.
        """
        select_sql = "SELECT * FROM lookup"

        result = self.database.get_cursor().execute(select_sql)

        while True:
            raw_data = result.fetchone()

            if raw_data is None:
                break

            item = self._row_to_item(raw_data)

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
        select_sql = "SELECT * FROM lookup"

        result = self.database.get_cursor().execute(select_sql)

        while True:
            raw_data = result.fetchone()
            item = self._row_to_item(raw_data)

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

        select_sql = "SELECT id, filename FROM lookup WHERE lookup_index=? LIMIT 1"

        result = self.database.get_cursor().execute(select_sql, [index])
        data = result.fetchone()

        # If we're in a state where the entry only exists in the memoized cache,
        # return status of removing that
        if data is None:
            return status

        filename = data[1]
        full_path = os.path.join(self.directory, filename)

        if os.path.isfile(full_path):
            os.remove(full_path)

        self.database.get_cursor().execute("DELETE FROM lookup WHERE lookup_index=?", [index])
        self.database.get_con().commit()

        # Failure to delete the filename given
        if os.path.isfile(full_path):
            return False

        return True

    def close(self):
        """Close the database."""
        if self.database is not None:
            self.database.close_db()
            self.database = None
