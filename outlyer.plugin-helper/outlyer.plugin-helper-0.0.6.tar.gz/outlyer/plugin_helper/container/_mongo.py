from outlyer.plugin_helper import container
from pymongo import MongoClient


def mongo_init(self, host=None, port=None, max_pool_size=100,
               document_class=dict, tz_aware=False, _connect=True,
               **kwargs):
    if container.is_container():
        if host in ('localhost', '127.0.0.1', '::1'):
            host = container.get_container_ip()
    return MongoClient.__old_init__(self, host, port, max_pool_size,
                                    document_class, tz_aware, _connect, **kwargs)


def patch():
    if not is_patched():
        MongoClient.__old_init__ = MongoClient.__init__
        MongoClient.__init__ = mongo_init


def unpatch():
    if is_patched():
        MongoClient.__init__ = MongoClient.__old_init__
        delattr(MongoClient, '__old_init__')


def is_patched():
    return hasattr(MongoClient, '__old_init__')
