'''
Module dbmanager.py
'''
QT = ['s', ]
QTFIELDS = {'s': 'textline', }
FTYP = ['TXT', 'TXN', 'INT', 'NUM', 'DAT', 'FK']
SQLTYP = {'TXT': 'TEXT NOT NULL', 'TXN': 'TEXT',
          'INT': 'INTEGER NOT NULL DEFAULT 0',
          'NUM': 'NUMERIC NOT NULL DEFAULT 0',
          'DAT': 'DATE NOT NULL',
          'FK': 'INTEGER NOT NULL REFERENCES %s(id)'}


class DbmanagerException(Exception):
    """Exception to use with class Dbmanager"""
    pass


class Dbmanager():
    '''
    Dbmanager class
    '''
    def __init__(self, user_version, application_id):
        self.user_version = user_version
        self.application_id = application_id
        self._tables = {}
        self._fields = {}
        self._fielda = {}  # Dictionary of array to keep field order

    def add_table(self, table, label, labelp, rpr=[], unifld=[]):
        '''
        Adds a new table
        table : The table Name
        label : The translated title of table
        labelp : The translated plural title of table
        rpr : List of table representation fields
        unifld : List of fields to be unique
        '''
        if table in self._tables:
            msg = 'Table %s already exists' % table
            raise DbmanagerException(msg)
        self._tables[table] = {'lbl': label,
                               'lblp': labelp,
                               'rpr': rpr,
                               'uniqfields': unifld}

    def add_field(self, table, field, label, typ='TXT', qt='s', unique=False):
        '''
        Adds a new field
        '''
        if table not in self._tables:
            msg = 'Table %s must be added to tables first' % table
            raise DbmanagerException(msg)
        if table not in self._fields:
            self._fields[table] = {}
            self._fielda[table] = []
        self._fields[table][field] = {'lbl': label,
                                      'typ': typ,
                                      'uni': unique}
        self._fielda[table].append(field)

    def get_joined_fields(self, table, only_rpr=False):
        """
        Returns string with joined fields
        """
        joiner = " || ' ' || "
        rprfields = self._tables[table]['rpr']
        tblfields = self.get_fields(table, with_id=False)
        if only_rpr:
            if rprfields:
                for field in tblfields:
                    if field not in tblfields:
                        msg = 'Field %s not in table %s' % (field, table)
                        raise DbmanagerException(msg)
            else:
                rprfields = tblfields
        else:
            rprfields = tblfields
        return joiner.join(rprfields)

    def rpr(self, table):
        '''
        Get sql of table representation
        '''
        if table not in self._tables:
            return ''
        rprfields = self._tables[table]['rpr']
        tblfields = self.get_fields(table, with_id=False)
        if rprfields:
            # Just check that exist
            for field in rprfields:
                if field not in tblfields:
                    msg = 'Field %s not in table %s' % (field, table)
                    raise DbmanagerException(msg)
        else:
            rprfields = tblfields
        sqlt = 'SELECT id, %s AS rpr FROM %s '
        sql = sqlt % (" || ' ' || ".join(rprfields), table)
        sql += "WHERE id=%s"
        return sql

    def get_labels(self, table):
        '''
        Returns a dictionary with fields: labels of table
        {'fld1': 'lbl1', 'fld2': 'lbl2', ...}
        '''
        if table not in self._fields:
            return {}
        tdic = {'id': 'ΑΑ'}
        for field in self._fields[table]:
            tdic[field] = self._fields[table][field]['lbl']
        return tdic

    def get_fields(self, table, with_id=True):
        '''
        Returns an ordered list with table fields
            with_id=True  : ['id', 'fld1', 'fld2', ...]
            with_id=False : ['fld1', 'fld2', ...]
        '''
        if table not in self._fields:
            return []
        tlist = []
        if with_id:
            tlist.append('id')
        for field in self._fielda[table]:
            tlist.append(field)
        return tlist

    def get_tables_fields(self):
        '''
        Returns a dictionary of tables: ordered list of table fields
        {'tabename': ['id', 'fld1', 'fld2', ...]}
        '''
        dic_list = {}
        for table in self._tables:
            dic_list[table] = self.get_fields(table)
        return dic_list

    def sql_create(self):
        '''
        Returns sql script for database creation
        '''
        sql = "BEGIN TRANSACTION;\n\n"
        sql += "PRAGMA user_version = %s;\n" % self.user_version
        sql += "PRAGMA application_id = %s;\n\n" % self.application_id
        for tbl in sorted(self._fields):
            sql += "CREATE TABLE IF NOT EXISTS %s (\n" % tbl
            tar = ["id INTEGER PRIMARY KEY"]
            for fld in self._fielda[tbl]:
                # Check if field is foreign key of the form table_id
                if fld.endswith('_id'):
                    ftable = fld[:-3]  # Remove the _id part
                    sqltyp = SQLTYP['FK'] % ftable
                else:
                    fldtype = self._fields[tbl][fld]['typ']
                    sqltyp = SQLTYP[fldtype]
                if self._fields[tbl][fld]['uni']:
                    sqltyp += ' UNIQUE'
                tar.append('\n%s %s' % (fld, sqltyp))
            if self._tables[tbl]['uniqfields']:
                unflds = self._tables[tbl]['uniqfields']
                tar.append('\nUNIQUE (%s)' % ', '.join(unflds))
            sql += ','.join(tar)
            sql += "\n);\n\n"
        sql += "COMMIT;"
        return sql

    def __repr__(self):
        stt = ''
        for tbl in sorted(self._tables):
            if tbl not in self._fields:
                continue
            stt += '%s %s %s\n' % (tbl, self._tables[tbl]['lbl'],
                                   self._tables[tbl]['lblp'])
            for fld in sorted(self._fields[tbl]):
                stt += '  %-10s %s\n' % (fld, self._fields[tbl][fld]['lbl'])
        return stt


if __name__ == "__main__":
    dbm = Dbmanager(user_version=2017, application_id=20170313)
    dbm.add_table('lmo', 'Λογαριασμός', 'Λογαριασμοί', ['lmo', 'lmop'])
    dbm.add_field('lmo', 'lmo', 'Λογαριασμός', unique=True)
    dbm.add_field('lmo', 'lmop', 'Περιγραφή')
    dbm.add_table('erg', 'Εργαζόμενος', 'Εργαζόμενοι', ['epo', 'ono'])
    dbm.add_field('erg', 'epo', 'Επώνυμο', 'TXN')
    dbm.add_field('erg', 'ono', 'Όνομα')
    dbm.add_field('erg', 'poso', 'Ποσό', 'NUM')
    dbm.add_field('erg', 'pat', 'Πατρώνυμο')
    dbm.add_field('erg', 'mit', 'Μητρώνυμο')
    dbm.add_field('erg', 'bdat', 'Ημ/νία γέννησης', 'DAT')
    dbm.add_field('erg', 'lmo_id', 'Λογαριασμός')
    dbm.add_table('trd', 'Κίνηση', 'Κινήσεις')
    dbm.add_field('trd', 'im_id', 'Ημερολόγιο')
    dbm.add_field('trd', 'lmo_id', 'Λογαριασμός')
    dbm.add_field('trd', 'per2', 'Περιγραφή')
    dbm.add_field('trd', 'xr', 'Χρέωση', 'NUM')
    # print(dbm.sql_create())
    # print(dbm.get_labels('erg'))
    # print(dbm.get_tables_fields())
    # print(dbm.get_fields('trd'))
    print(dbm.get_joined_fields('erg', only_rpr=True))
    print(dbm.sql_create())
