# -*- coding: utf-8 -*-

"""
This modules provides a clean interface for handling a table in a SQLite database.
"""

from __future__ import print_function

class DBWrapperTable(object):
    """This class provides utilities for creating and accessing a SQLite table
    """
    def __init__(self, con, table_name="transactions"):
        self.table_name = table_name
        self.con = con
        self.cursor = None
        self.delete_sql = "DELETE FROM {0}"
        self.create_sql = None
        self.update_sql = None

    def get_con(self):
        """Get the connection object.

        :returns: The connection object.
        """
        return self.con

    def get_cursor(self):
        """Get the database cursor.

        :returns: The cursor object
        """
        if self.cursor is None:
            self.cursor = self.get_con().cursor()
        return self.cursor

    def init_db(self, create_sql):
        """Initialize the database.

        :param create_sql: SQL to create the database.
        """
        cur = self.get_cursor()
        cur.execute(create_sql.format(self.table_name))
        self.get_con().commit()

    def empty_db(self):
        """Empty the database."""
        self.get_cursor().execute(self.delete_sql)
        self.get_con().commit()

    def set_update_sql(self, update_sql):
        """Set the update SQL to be used for update_db. Be careful, no security checks in place
        here.

        :param update_sql: The SQL to be used for an update.
        """
        self.update_sql = update_sql

    def update_db(self, params):
        """Update the database with the template provided earlier in set_update_sql().

        :param params: The list of SQL parameters.
        """
        if self.update_sql is None:
            raise RuntimeError("Call set_update_sql() first")
        self.get_cursor().execute(self.update_sql.format(self.table_name), params)
        self.get_con().commit()

    def num_rows(self):
        """Count the number of rows in the table.

        :returns: Number of rows in the table.
        """
        cur = self.get_cursor().execute("SELECT COUNT(*) from {0}".format(self.table_name))
        return cur.fetchone()[0]

    def print_db(self):
        """Print the contents of the table."""
        cur = self.get_cursor().execute("SELECT * from {0}".format(self.table_name))
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def close_db(self):
        """Commit results to database and close the database."""
        self.get_con().commit()
        self.get_cursor().close()
        self.get_con().close()
