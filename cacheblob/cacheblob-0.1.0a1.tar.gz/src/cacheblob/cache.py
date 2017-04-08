# -*- coding: utf-8 -*-

"""
This module implements a factory for the easy generation of handlers, identified by
strings.
"""

import cacheblob
import cacheblob.constants as C

class Cacheblob(object):
    """This class implements a factory to generate the right type of hander,
    such that the user does not need to know the module paths.
    """
    @staticmethod
    def cache(handler='handler', *args, **kwargs):
        """Create a handler from the given type requested.

        :param handler: The string name of a handler type.
            Must be one of: handler, gzip, plaintext, sqlite, mongo.
        :param args: Other arguments to pass through to handler.
        :param kwargs: Keyword arguments to pass through to handler.
        :returns: A handler of the given type.
        """

        if handler not in C.IMPLEMENTED_HANDLERS:
            raise ValueError("Handler \"{}\" is not defined".format(handler))
        if handler == 'handler':
            return cacheblob.handlers.Handler(*args, **kwargs)
        elif handler == 'gzip':
            return cacheblob.handlers.Gzip(*args, **kwargs)
        elif handler == 'plaintext':
            return cacheblob.handlers.Plaintext(*args, **kwargs)
        elif handler == 'sqlite':
            return cacheblob.handlers.SQLite(*args, **kwargs)
        elif handler == 'mongo':
            return cacheblob.handlers.mongo.Mongo(*args, **kwargs)
