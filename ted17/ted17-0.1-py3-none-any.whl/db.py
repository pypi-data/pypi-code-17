'''
This is obsolete.
'''
import sqlite3
import os
import logging
from .grup import grup
logger = logging.getLogger()


def app_id(dbf):
    """Get application_id"""
    if not os.path.isfile(dbf):
        return -10
    sql = 'pragma application_id;'
    try:
        rws = dataFromDB(dbf, sql)
        return rws[0][0]
    except:
        logger.exception("Something went wrong")
        return -9


def dataFromDB(dbf, sql):
    con = sqlite3.connect(dbf)
    con.create_function("grup", 1, grup)
    cur = con.cursor()
    cur.execute(sql)
    rws = cur.fetchall()
    cur.close()
    con.close()
    return rws


def execute_script(dbf, sqlscript):
    """Execute script"""
    con = sqlite3.connect(dbf)
    con.executescript(sqlscript)
    con.close()
    return True


def rowst(dbf, sql, with_column_names=False):
    '''
    Get a list of tuples of rows [(), (), ...]
    '''
    con = sqlite3.connect(dbf)
    cur = con.cursor()
    cur.execute(sql)
    if with_column_names:
        column_names = [t[0] for t in cur.description]
    rws = cur.fetchall()
    cur.close()
    con.close()
    if with_column_names:
        return column_names, rws
    else:
        return rws


def rowsd(dbf, sql):
    '''
    Get a list of dictionaries [{}, {}, ...]
    '''
    con = sqlite3.connect(dbf)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    list_of_dictionaries = []
    for row in rows:
        list_of_dictionaries.append(dict(zip(row.keys(), row)))
    return list_of_dictionaries


def db2dic(dbf, idv, tablemaster, tabledetail=None, key=None,
           remove_parent_id=True, id_at_end=True):
    '''
    dbf : sqlite database file path
    idv : id value of record
    tablemaster : Master table name
    tabledetail : Detail table name
    key : Foreign key Field in detail table that connects to mastertable
    '''
    if id_at_end:
        fkeytemplate = '%s_id'
    else:
        fkeytemplate = 'id_%s'
    if key:  # if we set key
        id_field = key
    else:  # Otherwise creates key automatically according to fkeytemplate
        id_field = fkeytemplate % tablemaster
    sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
    sql2 = "SELECT * FROM %s WHERE %s='%s'" % (tabledetail, id_field, idv)
    con = sqlite3.connect(dbf)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql1)
    rows = cur.fetchall()
    if rows:
        dic = dict(zip(rows[0].keys(), rows[0]))
    else:
        return {}
    if tabledetail:
        cur.execute(sql2)
        rows = cur.fetchall()
        dic['zlines'] = []
        for i, row in enumerate(rows):
            dic['zlines'].append(dict(zip(row.keys(), row)))
            if (id_field in dic['zlines'][i]) and remove_parent_id:
                del dic['zlines'][i][id_field]
    cur.close()
    con.close()
    return dic


def sql_ins_upd(table, adic):
    '''
    Returns update or insert sql according id
    if id = 0 returns insert sql
    if id <> 0 returns update sql
    '''
    fields = []
    values = []
    ufldva = []
    adic['id'] = adic.get('id', 0)
    for el in adic.keys():
        if el == 'id':
            continue
        if el == 'zlines':
            continue
        fields.append(el)
        if '(SELECT MAX(id) FROM' in ('%s' % adic[el]):
            values.append("%s" % adic[el])
        else:
            values.append("'%s'" % adic[el])
        ufldva.append("%s='%s'" % (el, adic[el]))
    if '_d_' in adic:
        sql = 'DELETE FROM %s WHERE id=%s;'
        return sql % (table, adic['id'])
    if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
        sql = "INSERT INTO %s (%%s) VALUES (%%s);" % table
        return sql % (', '.join(fields), ', '.join(values))
    else:
        sql = "UPDATE %s SET %s WHERE id=%s;"
        return sql % (table, ', '.join(ufldva), adic['id'])


def md2sql(tmaster, tdetail, adic, id_at_end=True):
    '''
    Master-Detail to sql
    tmaster : master table name
    tdetail : detail table name
    adic    : dictionary to translate to sql. Keys represent
              table fields
    id_at_end : if foreign key looks like id_* then False
                if foreign key looks like *_id then True
    '''
    sql = sql_ins_upd(tmaster, adic) + '\n'
    if id_at_end:
        fkey = '%s_id'
    else:
        fkey = 'id_%s'
    for el in adic['zlines']:
        if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
            el[fkey % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
        else:
            el[fkey % tmaster] = adic['id']
        sql += sql_ins_upd(tdetail, el) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;\n'
