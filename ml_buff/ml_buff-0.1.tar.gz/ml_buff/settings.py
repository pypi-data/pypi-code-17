DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'postgres',
    'database': 'ml_buff'
}

try:
	from local_settings import *
except ImportError as e:
	pass
