'''
Module db_sql.py
Creates insert, update, delete sql from dictionaries
'''


def dic2sql(table, adic):
    '''
    Dictionary to Sql.

    :param table: Table name
    :param adic: dictionary with key names same with table field names
    :return: sql according to input parameter adic.

    If adic['id'] == 0 returns insert sql

    If adic['id] != 0 returns update sql

    If there is adic['_d_'] returns delete sql
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


def dic2sql_md(tmaster, tdetail, adic, id_at_end=True):
    '''
    Dictionary to transactional SQL.

    :param tmaster: master table name
    :param tdetail: detail table name
    :param adic: dictionary to translate to sql. Keys represent table fields
    :param id_at_end: tmaster_id or id_tmaster
    :return: SQL
    '''
    sql = dic2sql(tmaster, adic) + '\n'
    if id_at_end:
        fkey = '%s_id'
    else:
        fkey = 'id_%s'
    for el in adic['zlines']:
        if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
            el[fkey % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
            assert el.get('id', 0) == 0
        else:
            el[fkey % tmaster] = adic['id']
        # if master is marked for deletion do the same to detail
        if '_d_' in adic:
            el['_d_'] = 1
            assert 'id' in el
        sql += dic2sql(tdetail, el) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;'
