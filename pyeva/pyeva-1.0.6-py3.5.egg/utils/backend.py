from eva.utils.importlib import import_module
from eva.conf import settings

def load_auth_backend():
    b = import_module(settings.BACKENDS["auth"])
    return b
