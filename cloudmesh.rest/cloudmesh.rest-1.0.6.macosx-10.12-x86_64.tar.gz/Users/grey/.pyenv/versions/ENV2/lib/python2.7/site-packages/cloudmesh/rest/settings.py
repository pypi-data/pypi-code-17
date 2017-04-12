
cluster = {
    'schema': {
        'frontend': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'node',
                'field': '_id',
                'embeddable': True
            }
        },
        'computenodes': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'node',
                    'field': '_id',
                    'embeddable': True
                }
            }
        }
    }
}

node = {
    'schema': {
        'name': {
            'type': 'string'
        },
        'label': {
            'type': 'string'
        },
        'ncpu': {
            'type': 'integer'
        },
        'RAM': {
            'type': 'string'
        },
        'disk': {
            'type': 'string'
        },
        'NIC': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'nic',
                    'field': '_id',
                    'embeddable': True
                }
            }
        }
    }
}

nic = {
    'schema': {
        'name': {
            'type': 'string'
        },
        'mac': {
            'type': 'string'
        },
        'IP': {
            'type': 'string'
        }
    }
}



eve_settings = {
    'MONGO_HOST': 'localhost',
    'MONGO_DBNAME': 'testing',
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'BANDWIDTH_SAVER': False,
    'DOMAIN': {
        'cluster': cluster,
        'node': node,
        'nic': nic,
    },
}
