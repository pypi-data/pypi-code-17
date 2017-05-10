'''
Module db.py
Connect to sqlite database and perform crud functions

Example::

>>> from ted17 import db_context_manager as dbc
>>> with dbc.SqliteManager('path/to/sql3file') as db:
>>>     db.select('SELECT * from tbl1')
'''
import sqlite3
from .grup import grup


def dataFromDB(dbf, sql):
    """Get data from database

    :param dbf: Database file path
    :param sql: SQL to run
    :return: list of tuples [(), (), ...]
    """
    con = sqlite3.connect(dbf)
    con.create_function("grup", 1, grup)
    cur = con.cursor()
    cur.execute(sql)
    rws = cur.fetchall()
    cur.close()
    con.close()
    return rws


class SqliteManager:
    '''
    Context manager class
    '''
    def __init__(self, dbfile):
        self.dbf = dbfile  #: This is a test
        self.in_context_mode = False
        self.active = False
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(self.dbf)
        self.con.create_function("grup", 1, grup)
        self.cur = self.con.cursor()
        self.in_context_mode = True
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.cur.close()
            self.con.close()
        self.in_context_mode = False

    def _open(self):
        if self.in_context_mode:
            return
        if not self.active:
            self.con = sqlite3.connect(self.dbf)
            self.cur = self.con.cursor()
            self.active = True

    def _close(self):
        if self.in_context_mode:
            return
        if self.active:
            self.cur.close()
            self.con.close()
        self.cur = None
        self.con = None
        self.active = False

    def script(self, sqlscript):
        """Execute an sql script against self.dbf

        :param sqlscript: SQL to run
        :return: Nothing
        """
        self._open()
        self.con.executescript(sqlscript)
        self._close()
        return True

    def application_id(self):
        '''Get application_id from database file

        :return: application_id or -9
        '''
        sql = 'PRAGMA application_id;'
        self._open()
        try:
            app_id = self.select(sql)[0][0]
        except:
            app_id = 0
        self._close()
        return app_id

    def set_application_id(self, idv):
        '''Set application_id to database file

        :param idv: application_id value to set
        :return: nothing
        '''
        self._open()
        self.script('PRAGMA application_id = %s;' % idv)
        self._close()

    def user_version(self):
        '''Get user_version from database file

        :return: user_version or -9
        '''
        sql = 'PRAGMA user_version;'
        self._open()
        try:
            user_version = self.select(sql)[0][0]
        except:
            user_version = 0
        self._close()
        return user_version

    def set_user_version(self, version):
        '''Set user_version to database file

        :param version: version value to set
        :return: Nothing
        '''
        self._open()
        self.script('PRAGMA user_version = %s;' % version)
        self._close()

    def select(self, sql):
        '''Get a list of tuples with data

        :param sql: SQL to run
        :return: List of tuples of rows
        '''
        self._open()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self._close()
        return rows

    def select_with_names(self, sql):
        '''Get a tuple with column names and a list of tuples with data

        :param sql: The sql to execute
        :return: (columnNam1, ...) [(dataLine1), (dataLine2), ...]
        '''
        self._open()
        self.cur.execute(sql)
        column_names = tuple([t[0] for t in self.cur.description])
        rows = self.cur.fetchall()
        self._close()
        return column_names, rows

    def select_as_dict(self, sql):
        '''Get a list of dictionaries

        :param sql: The sql to execute
        :return: [{}, {}, ...]
        '''
        self._open()
        self.cur.execute(sql)
        column_names = [t[0] for t in self.cur.description]
        rows = self.cur.fetchall()
        diclist = []
        for row in rows:
            dic = {}
            for i, col in enumerate(row):
                dic[column_names[i]] = col
            diclist.append(dic)
        diclen = len(diclist)
        self._close()
        if diclen > 0:
            return diclist
        return [{}]

    def select_master_detail(self,
                             idv,
                             tablemaster,
                             tabledetail=None,
                             id_at_end=True):
        '''
        Get a specific record from table tablemaster.
        If we pass it a tabledetail value, it gets detail records too.

        :param idv: id value of record
        :param tablemaster: Master table name
        :param tabledetail: Detail table name
        :param id_at_end: If True Foreign key is like tablemaster_id
         else is like id_mastertable
        :return: dictionary with values
        '''
        if id_at_end:
            fkeytemplate = '%s_id'
        else:
            fkeytemplate = 'id_%s'

        id_field = fkeytemplate % tablemaster
        sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
        sql2 = "SELECT * FROM %s WHERE %s='%s'" % (tabledetail, id_field, idv)
        dic = self.select_as_dict(sql1)[0]
        ldic = len(dic)
        if ldic == 0:
            return dic
        if tabledetail:
            dic['zlines'] = self.select_as_dict(sql2)
            # Remove id_field key
            for elm in dic['zlines']:
                del elm[id_field]
        return dic

    def tables(self):
        """A tuple with database tables"""
        sql = "select name from sqlite_master where type = 'table';"
        val = self.select(sql)
        tbl = [el[0] for el in val]
        tbl.sort()
        return tuple(tbl)

    def views(self):
        """A Tuple with database views"""
        sql = "select name from sqlite_master where type = 'view';"
        val = self.select(sql)
        viw = [el[0] for el in val]
        viw.sort()
        return tuple(viw)

    def fields(self, table_or_view):
        """A Tuple with table or view fields

        :param table_or_view: Table or View name
        """
        sql = 'SELECT * FROM %s LIMIT 0' % table_or_view
        self._open()
        self.cur.execute(sql)
        column_names = [t[0] for t in self.cur.description]
        self._close()
        return tuple(column_names)
