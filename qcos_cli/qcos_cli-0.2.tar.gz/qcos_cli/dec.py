from functools import wraps


def _check_config(config):
    for key, val in config.items():
        if not val:
            if key == 'appid':
                export_key = 'QCOS_APPID'
            elif key == 'secret_id':
                export_key = 'QCOS_SECRET_ID'
            elif key == 'secret_key':
                export_key = 'QCOS_SECRET_KEY'
            elif key == 'region':
                export_key = 'QCOS_REGION'
            elif key == 'bucket_name':
                export_key = 'QCOS_BUCKET_NAME'
            raise AttributeError(
                '{key} is not set, should export {export_key}=xxxxxx'.format(key=key,
                                                                             export_key=export_key))


def check_config(config):
    def real_dec(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _check_config(config)
            return fn(*args, **kwargs)

        return wrapper

    return real_dec


class CheckConfig(object):
    def __init__(self, config):
        self.config = config

    def __call__(self, cls):
        for key, val in vars(cls).items():
            if callable(val) and not key.startswith('__'):
                setattr(cls, key, check_config(self.config)(val))
        return cls
