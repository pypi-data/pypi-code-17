import datetime
from urlparse import urlparse

from django.conf import settings

import redis
from emitter import Emitter


class SafeEmitter(Emitter):
    emitter = None

    def make_safe(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.make_safe(value)
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
        return data

    def EmitSafe(self, event, data, **kwargs):
        return self.Emit(event, self.make_safe(data), **kwargs)


def get_emitter():
    if not SafeEmitter.emitter:
        if hasattr(settings, "SOCKETIO_REDIS"):
            if settings.SOCKETIO_REDIS:
                SafeEmitter.emitter = SafeEmitter(settings.SOCKETIO_REDIS)
        else:
            location = urlparse(settings.CACHES['default']['LOCATION'])
            client = redis.StrictRedis(**{
                "host": location.hostname,
                "port": location.port,
                "db": location.path.strip("/") or 0
            })
            SafeEmitter.emitter = SafeEmitter({
                "client": client
            })
    return SafeEmitter.emitter
