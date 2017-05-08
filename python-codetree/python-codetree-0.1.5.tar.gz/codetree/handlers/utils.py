import logging
from subprocess import (
    STDOUT,
    check_output,
    CalledProcessError
)
from six.moves.urllib.parse import urlparse

from .basic import SourceHandler
from .exceptions import CommandFailure, DuplicateHandlerError, NoSuchHandlerError


def handler_types(handler_class=None):
    "Build a registry of handlers"
    if handler_class is None:
        handler_class = SourceHandler
    types = {}
    for subclass in handler_class.__subclasses__():
        for scheme in subclass.schemes:
            if scheme in types:
                new_handler = subclass.__name__
                old_handler = types[scheme].__name__
                raise DuplicateHandlerError("{} and {}".format(old_handler, new_handler))
            else:
                types[scheme] = subclass
    return types


def handler_for_url(url):
    """ Build a handler based on the given URL
    :param url: Source url
    :return: A SourceHandler object of the right type
    """
    if getattr(handler_types, "cache", None) is None:
        handler_types.cache = handler_types()
    scheme = urlparse(url).scheme
    if scheme in handler_types.cache:
        return handler_types.cache[scheme](url)
    raise NoSuchHandlerError("No handler found for URL: {}".format(url))


def log_failure(cmd, message, fatal=False):
    try:
        if message is not None:
            logging.info(message)
        check_output(cmd, stderr=STDOUT, universal_newlines=True)
        return True
    except CalledProcessError as e:
        logging.error(e.output)
        if fatal:
            raise CommandFailure(e.output, e)
        else:
            return False
    except OSError as e:
        logging.error(e.strerror)
        if fatal:
            raise CommandFailure(e.strerror, e)
        else:
            return False


def strip_trailing_slash(value):
    if value[-1] == "/":
        return value[:-1]
    return value
