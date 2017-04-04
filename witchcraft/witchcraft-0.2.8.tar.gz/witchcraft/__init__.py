from witchcraft.utils import seekable
from witchcraft.upsert import prepare_table, upsert_data, insert_data
from witchcraft.combinators import query, template

#TODO: allow using serial primary key without defining value in data set

def upsert(connection, schema_name, table_name, data_points, primary_keys):
    #TODO: use seekable from utils and call prepare table (to create new columns) in batches (10000)
    data_points = list(data_points)

    if len(data_points) == 0:
        return

    prepare_table(connection, schema_name, table_name, data_points, primary_keys)
    upsert_data(connection, schema_name, table_name, data_points, primary_keys)


def insert(connection, schema_name, table_name, data_points, primary_keys):
    #TODO: use seekable from utils and call prepare table (to create new columns) in batches (10000)
    data_points = list(data_points)

    if len(data_points) == 0:
        return

    prepare_table(connection, schema_name, table_name, data_points, primary_keys)
    insert_data(connection, schema_name, table_name, data_points)

