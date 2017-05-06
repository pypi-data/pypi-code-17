INT_PRIM = 'int'
LONG_PRIM = 'long'
DOUBLE_PRIM = 'double'
FLOAT_PRIM = 'float'
BYTE_PRIM = 'byte'
BOOLEAN_PRIM = 'boolean'

STRING = 'String'
INTEGER = 'Integer'
LONG = 'Long'
DOUBLE = 'Double'
FLOAT = 'Float'
BYTE = 'Byte'
BOOLEAN = 'Boolean'

DATE = 'Date'
TIMESTAMP = 'Timestamp'

java_types = {
    'string': STRING,
    'str': STRING,
    'int': INTEGER,
    'integer': INTEGER,
    'long': LONG,
    'date': DATE,
    'timestamp': TIMESTAMP,
}

dependencies = {
    DATE: 'java.util.Date',
    TIMESTAMP: 'java.sql.Timestamp'
}


def fetch_type(type_string):
    key = type_string.lower()
    return java_types[key] if key in java_types else None


def fetch_dependency(java_type):
    return dependencies[java_type] if java_type in dependencies else None
