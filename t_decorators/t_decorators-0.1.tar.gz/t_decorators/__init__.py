#!/usr/bin/env python

import uuid
from functools import wraps

# TODO: move to a file that denotes this only applies to instancem methods
def log_exception(logger_name):
    '''
    Class instance method decorator for logging an unhandled exception before
    rethrowing.
    '''
    def _log_exception(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as ex:
                logger = getattr(self, logger_name)
                logger.exception('Encountered an unexpected exception.')
                raise
        return wrapper
    return _log_exception


def request_id_class_method(func):
    ''''
    Classmethod decorator for generating a thread local request id.
    '''
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        kwargs['request_id'] = uuid.uuid4()
        return func(cls, *args, **kwargs)
    return wrapper
