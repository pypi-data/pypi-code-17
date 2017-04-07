VERSION = (0, 99, 17)


def get_version():
    return u'.'.join((unicode(num) for num in VERSION))

__version__ = get_version()
