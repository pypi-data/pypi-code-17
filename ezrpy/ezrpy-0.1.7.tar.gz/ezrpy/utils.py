import re

FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


def to_url(name):
    sub = FIRST_CAP_RE.sub(r'\1-\2', name)
    return ALL_CAP_RE.sub(r'\1-\2', sub).lower()


class Logger(object):
    DEBUG = 1
    MINIMAL = 0

    level = 1

    @staticmethod
    def debug(msg, *objects):
        if Logger.level >= Logger.DEBUG:
            print(msg % objects)
