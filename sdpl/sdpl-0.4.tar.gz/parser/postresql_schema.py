__author__ = 'Bohdan Mushkevych'

from schema.sdpl_schema import Schema, Field, MIN_VERSION_NUMBER, VARCHAR_DEFAULT_LENGTH, FieldType
from parser.data_store import DataStore

PGSQL_MAPPING = {
    FieldType.INTEGER.name: 'INTEGER',
    FieldType.LONG.name: 'BIGINT',
    FieldType.FLOAT.name: 'DOUBLE PRECISION',
    FieldType.CHARARRAY.name: 'VARCHAR',
    FieldType.BYTEARRAY.name: 'BYTEA',
    FieldType.BOOLEAN.name: 'BOOLEAN',
    FieldType.DATETIME.name: 'TIMESTAMP',
}


def parse_field(field: Field):
    pgsql_type = PGSQL_MAPPING[field.field_type]
    if field.field_type == 'CHARARRAY':
        length = field.max_length if field.max_length else VARCHAR_DEFAULT_LENGTH
        pgsql_type += '({0})'.format(length)

    out = '{0}\t{1}'.format(field.name, pgsql_type)
    if not field.is_nullable:
        out += '\t{0}'.format('NOT NULL')
    if field.is_unique:
        out += '\t{0}'.format('UNIQUE')
    if field.is_primary_key:
        out += '\t{0}'.format('PRIMARY KEY')
    if field.default:
        out += '\t{0}\t{1}'.format('DEFAULT', field.default)

    return out


def parse_schema(schema: Schema, max_version=MIN_VERSION_NUMBER):
    filtered_fields = [f for f in schema.fields if f.version <= max_version]
    out = ',\n    '.join([parse_field(field) for field in filtered_fields])
    out = '\n    ' + out + '\n'
    return out


def parse_datasink(data_sink: DataStore):
    field_names = [f.name for f in data_sink.relation.schema.fields]
    values = ['?' for _ in range(len(field_names))]

    out = "REGISTER /var/lib/sdpl/postgresql-42.0.0.jar;\n"
    out += "REGISTER /var/lib/sdpl/piggybank-0.16.0.jar;\n"
    out += "STORE {0} INTO 'hdfs:///unused-ignore' ".format(data_sink.relation.name)
    out += "USING org.apache.pig.piggybank.storage.DBStorage(\n"
    out += "    'org.postgresql.Driver',\n"
    out += "    'jdbc:postgresql://{0}:{1}/{2}',\n".format(data_sink.data_repository.host,
                                                           data_sink.data_repository.port,
                                                           data_sink.data_repository.db)
    out += "    '{0}', '{1}',\n".format(data_sink.data_repository.user, data_sink.data_repository.password)
    out += "    'INSERT INTO {0} ({1}) VALUES ({2})'\n".format(data_sink.table_name,
                                                               ','.join(field_names), ','.join(values))
    out += ');'
    return out


def parse_datasource(data_source: DataStore):
    raise NotImplementedError('postgresql_schema.data_source is not supported')


def compose_ddl(table_name: str, schema: Schema, max_version: int):
    out = 'CREATE TABLE IF NOT EXISTS {0} ('.format(table_name)
    out += parse_schema(schema, max_version)
    out += ');\n'
    return out
