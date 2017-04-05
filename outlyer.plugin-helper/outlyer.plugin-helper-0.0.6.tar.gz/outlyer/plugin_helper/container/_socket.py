# noinspection PyProtectedMember
from socket import _socketobject
from outlyer.plugin_helper.container import get_container_ip, is_container, is_localhost


# noinspection PyTypeChecker
def connect(self, address):
    if is_container():
        if isinstance(address, tuple) and is_localhost(address[0]):
            # handle AF_INET and AF_INET6
            address = list(address)
            address[0] = get_container_ip()
            address = tuple(address)
        elif isinstance(address, basestring) and is_localhost(address):
            # handle AF_UNIX
            address = get_container_ip()
    getattr(_socketobject, '_connect')(self, address)


def patch():
    if not is_patched():
        _socketobject._connect = _socketobject.connect
        _socketobject.connect = connect


def unpatch():
    if is_patched():
        _socketobject.connect = getattr(_socketobject, '_connect')
        delattr(_socketobject, '_connect')


def is_patched():
    return hasattr(_socketobject, '_connect')
