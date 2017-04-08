# -*- coding: utf-8 -*-

"""
This module allows us to manage a series of tables in a SQLite database.
"""

from __future__ import absolute_import

import sqlite3
import six

from . import db_wrapper_table

class DBWrapper(object):
    """DBWrapper manages a series of DBWrapperTable objects."""
    def __init__(self, name="results.db", pytypes=False):
        self.db_name = name
        self.con = None
        self.cursor = None
        self.table_list = {}
        self.pytypes = pytypes

    def get_con(self):
        """Access or initiate the sqlite3 connection.

        :returns: The sqlite3 connection.
        """
        if self.con is None:
            if self.pytypes:
                self.con = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
            else:
                self.con = sqlite3.connect(self.db_name)
            self.con.text_factory = lambda x: six.text_type(x, 'utf-8', 'ignore')
        return self.con

    def get_cursor(self):
        """Access or initiate the sqlite3 cursor.

        :returns: The sqlite3 cursor.
        """
        if self.cursor is None:
            self.cursor = self.get_con().cursor()
        return self.cursor

    def add_table(self, table_name):
        """Add a table to the collection.

        :param table_name: The name you will refer to the table by.
        """
        self.table_list[table_name] = db_wrapper_table.DBWrapperTable(con=self.get_con(),
                                                                      table_name=table_name)

    def empty_all_dbs(self):
        """Empty all of the tables."""
        for table in self.table_list:
            table.empty_db()

    def close_db(self):
        """Commit results to database and close the database."""
        self.get_con().commit()
        self.get_cursor().close()
        self.get_con().close()

    # The following methods are wrappers around the table-specific methods

    def init_table(self, table_name, create_sql):
        """Initialize a table.

        :param table_name: The name you will refer to the table by.
        :param create_sql: The SQL used to initialize the database.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].init_db(create_sql)

    def empty_db(self, table_name):
        """Empty a given table.

        :param table_name: The name of the table.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].empty_db()

    def set_update_sql(self, table_name, update_sql):
        """Set the update SQL to be used for update_db for a given table. Be careful, no
        security checks in place here.

        :param table_name: The name of the table.
        :param update_sql: The SQL to be used for an update.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].set_update_sql(update_sql)

    def update_db(self, table_name, params):
        """Update the database with the template provided earlier in set_update_sql().

        :param table_name: The name of the table.
        :param params: The list of SQL parameters.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].update_db(params)

    def num_rows(self, table_name):
        """Count the number of rows in the table.

        :param table_name: The name of the table.
        :returns: Number of rows in the table.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].num_rows()

    def print_db(self, table_name):
        """Print the contents of a table.

        :param table_name: The name of the table.
        """
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].print_db()
