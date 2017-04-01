import csv
import sqlite3
from collections import OrderedDict

class NoTableException(Exception):
    def __init__(self, table):
        Exception.__init__(self, "Table '{}' does not exist".format(table))


class SQLEx(object):
    """
    sqlite model
    https://docs.python.org/2/library/sqlite3.html
    """

    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)

    def __call__(self, sql, *args):
        c = self.conn.cursor()
        c.execute(sql, args)
        self.conn.commit()
        try:
            return c.fetchall()
        except Exception as e:
            raise e

    def __del__(self):
        self.conn.close()

    def tables(self):
        """
        returns table names in database
        """
        # http://stackoverflow.com/questions/82875/how-to-list-the-tables-in-an-sqlite-database-file-that-was-opened-with-attach

        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self(sql)
        return sum([list(item) for item in tables], [])

    def ensure_table(self, table):
        """
        ensure that `table` exists;
        if not, raise 1NoTableException
        """

        if table not in self.tables():
            raise NoTableException(table)

    def columns(self, table):
        """
        returns columns for `table`
        """

        self.ensure_table(table)

        sql = "PRAGMA table_info({})".format(table)
        data = self(sql)
        # (Pdb) pp(columns)
        # [(0, u'ROWID', u'INTEGER', 0, None, 1),
        #  (1, u'address', u'TEXT', 0, None, 0),
        #  (2, u'date', u'INTEGER', 0, None, 0),
        NAME_INDEX = 1
        TYPE_INDEX = 2
        return OrderedDict([(row[NAME_INDEX], row[TYPE_INDEX])
                            for row in data])


    def table2csv(self, table, fp, header=False):
        """
        export `table` to `fp` file object in CSV format
        """
        # TODO: option to add column headers

        # sanity
        self.ensure_table(table)

        # get whole table
        sql = 'select * from {table}'.format(table=table)
        rows = self(sql)

        if header:
            # export header as first row, if specified
            _header = self.columns(table).keys()
            if _header:
                _header[0] = '#{}'.format(_header[0])
            rows.insert(0, _header)

        # decode unicde because the CSV module won't
        # http://stackoverflow.com/questions/22733642/how-to-write-a-unicode-csv-in-python-2-7
        rows = [[unicode(s).encode("utf-8") for s in row]
                for row in rows]

        # write
        writer = csv.writer(fp)
        writer.writerows(rows)

