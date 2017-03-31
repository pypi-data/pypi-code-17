import web
import config

db = config.db

def get_all_table_name():
    try:
        return db.select('table_name')
    except:
        return None

def get_table_name(primary_key):
    try:
        return db.select('table_name', where='primary_key=$primary_key', vars=locals())[0]
    except:
        return None

def delete_table_name(primary_key):
    try:
        return db.delete('table_name', where='primary_key=$primary_key', vars=locals())
    except:
        return None

def insert_table_name(fields):
    try:
        db.insert('table_name',values)
    except:
        return None

def edit_table_name(fields_all):
    try:
        db.update('table_name',values_all,
                  where='primary_key=$primary_key',
                  vars=locals())
    except:
        return None
