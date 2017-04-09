import time
import functools

from dmu_utils.misc import get_call_repr


class Duration(object):

    def __init__(self, logger_method, template=None, log_args=False):
        self.logger_method = logger_method
        self.template = template
        self.log_args = log_args
        self.start_time = None

    def __call__(self, func_or_meth):
        @functools.wraps(func_or_meth)
        def wrapper(*args, **kwargs):
            if self.template:
                template = self.template
            else:
                if self.log_args:
                    # TODO(dmu) HIGH: Handle method printing
                    template = get_call_repr(func_or_meth, args, kwargs)
                else:
                    template = get_call_repr(func_or_meth)

            with Duration(self.logger_method, template=template, log_args=self.log_args):
                return func_or_meth(*args, **kwargs)

        return wrapper

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        finish_time = time.time()

        message = (self.template or 'block') + ' is done in {:.06f} seconds'.format(
            finish_time - self.start_time)

        if exc_type:
            message += ' with {!r}'.format(exc_value)

        self.logger_method(message)
