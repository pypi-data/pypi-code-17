import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ATOMIC_REQUESTS = True
INSTALLED_APPS = [
    'corenetwork',
]

DATABASE_ROUTERS = ['corenetwork.utils.db_router.BasicRouter']

SECRET_KEY = 'none'
ROOT_URLCONF = 'corenode.urls'

USE_TZ = False
TIME_ZONE = 'UTC'

# Load main configuration file with Django settings
import imp
import sys
try:
    sys.dont_write_bytecode = True
    coreConfig = imp.load_source('config', '/etc/corenode/config.py')
except Exception as e:
    print('Failed to load configuration: %s' % str(e))
    sys.exit(1)

for variable in dir(coreConfig):
    setattr(sys.modules[__name__], variable, getattr(coreConfig, variable))
